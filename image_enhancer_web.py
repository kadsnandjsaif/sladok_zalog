#!/usr/bin/env python3
"""
Веб-интерфейс для улучшения качества изображений
"""

from flask import Flask, request, render_template_string, send_file, flash, redirect, url_for
import os
import tempfile
from werkzeug.utils import secure_filename
from image_enhancer import ImageEnhancer
import shutil

app = Flask(__name__)
app.secret_key = 'image_enhancer_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Улучшение качества изображений</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .upload-area {
            border: 3px dashed #ccc;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            border-color: #667eea;
            background-color: #f8f9ff;
        }
        .upload-area.dragover {
            border-color: #667eea;
            background-color: #e8f0fe;
        }
        input[type="file"] {
            margin: 10px 0;
        }
        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        .control-group {
            display: flex;
            flex-direction: column;
        }
        label {
            font-weight: bold;
            margin-bottom: 5px;
            color: #555;
        }
        input[type="range"] {
            width: 100%;
            margin: 5px 0;
        }
        .range-value {
            text-align: center;
            color: #667eea;
            font-weight: bold;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
            margin: 10px 5px;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .alert {
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        .alert-success {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }
        .alert-error {
            background-color: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }
        .result-section {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
        }
        .download-btn {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        }
        .progress {
            display: none;
            width: 100%;
            height: 20px;
            background-color: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            margin: 20px 0;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Улучшение качества изображений</h1>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-error">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="post" enctype="multipart/form-data" id="enhanceForm">
            <div class="upload-area" id="uploadArea">
                <p>📁 Перетащите изображение сюда или нажмите для выбора файла</p>
                <input type="file" name="file" accept="image/*" required id="fileInput">
                <p><small>Поддерживаемые форматы: JPG, PNG, GIF, BMP, TIFF, WebP</small></p>
            </div>
            
            <div class="controls">
                <div class="control-group">
                    <label for="denoise">🔇 Удаление шума:</label>
                    <input type="range" id="denoise" name="denoise" min="0" max="30" value="10" oninput="updateValue('denoise')">
                    <div class="range-value" id="denoise-value">10</div>
                </div>
                
                <div class="control-group">
                    <label for="sharpen">⚡ Резкость:</label>
                    <input type="range" id="sharpen" name="sharpen" min="0.5" max="3.0" step="0.1" value="1.2" oninput="updateValue('sharpen')">
                    <div class="range-value" id="sharpen-value">1.2</div>
                </div>
                
                <div class="control-group">
                    <label for="contrast">🌟 Контрастность:</label>
                    <input type="range" id="contrast" name="contrast" min="0.5" max="3.0" step="0.1" value="1.2" oninput="updateValue('contrast')">
                    <div class="range-value" id="contrast-value">1.2</div>
                </div>
                
                <div class="control-group">
                    <label for="gamma">💡 Гамма:</label>
                    <input type="range" id="gamma" name="gamma" min="0.5" max="2.0" step="0.1" value="1.1" oninput="updateValue('gamma')">
                    <div class="range-value" id="gamma-value">1.1</div>
                </div>
                
                <div class="control-group">
                    <label for="saturation">🎨 Насыщенность:</label>
                    <input type="range" id="saturation" name="saturation" min="0.5" max="2.0" step="0.05" value="1.15" oninput="updateValue('saturation')">
                    <div class="range-value" id="saturation-value">1.15</div>
                </div>
                
                <div class="control-group">
                    <label for="upscale">📏 Увеличение:</label>
                    <input type="range" id="upscale" name="upscale" min="1.0" max="4.0" step="0.1" value="1.5" oninput="updateValue('upscale')">
                    <div class="range-value" id="upscale-value">1.5x</div>
                </div>
            </div>
            
            <div class="progress" id="progress">
                <div class="progress-bar" id="progressBar"></div>
            </div>
            
            <div style="text-align: center;">
                <button type="submit" id="enhanceBtn">🚀 Улучшить изображение</button>
                <button type="button" onclick="resetForm()">🔄 Сбросить</button>
            </div>
        </form>
        
        {% if result_file %}
        <div class="result-section">
            <h3>✅ Обработка завершена!</h3>
            <p>Изображение успешно улучшено.</p>
            <div style="text-align: center;">
                <a href="{{ url_for('download_file', filename=result_file) }}" class="download-btn" style="text-decoration: none; color: white; display: inline-block; padding: 15px 30px; border-radius: 8px;">
                    💾 Скачать улучшенное изображение
                </a>
            </div>
        </div>
        {% endif %}
    </div>

    <script>
        function updateValue(id) {
            const input = document.getElementById(id);
            const display = document.getElementById(id + '-value');
            let value = input.value;
            if (id === 'upscale') {
                value += 'x';
            }
            display.textContent = value;
        }
        
        function resetForm() {
            document.getElementById('enhanceForm').reset();
            ['denoise', 'sharpen', 'contrast', 'gamma', 'saturation', 'upscale'].forEach(updateValue);
        }
        
        // Drag and drop functionality
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
            }
        });
        
        // Form submission with progress
        document.getElementById('enhanceForm').addEventListener('submit', function(e) {
            const progress = document.getElementById('progress');
            const progressBar = document.getElementById('progressBar');
            const enhanceBtn = document.getElementById('enhanceBtn');
            
            progress.style.display = 'block';
            enhanceBtn.disabled = true;
            enhanceBtn.textContent = '⏳ Обработка...';
            
            // Simulate progress
            let width = 0;
            const interval = setInterval(() => {
                width += Math.random() * 10;
                if (width >= 90) {
                    clearInterval(interval);
                    width = 90;
                }
                progressBar.style.width = width + '%';
            }, 200);
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result_file = None
    
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('Файл не выбран')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Get parameters from form
                denoise = int(request.form.get('denoise', 10))
                sharpen = float(request.form.get('sharpen', 1.2))
                contrast = float(request.form.get('contrast', 1.2))
                gamma = float(request.form.get('gamma', 1.1))
                saturation = float(request.form.get('saturation', 1.15))
                upscale = float(request.form.get('upscale', 1.5))
                
                # Save uploaded file
                filename = secure_filename(file.filename)
                temp_dir = tempfile.mkdtemp()
                input_path = os.path.join(temp_dir, filename)
                file.save(input_path)
                
                # Enhance image
                enhancer = ImageEnhancer()
                output_path = enhancer.enhance_image_comprehensive(
                    input_path,
                    denoise_strength=denoise,
                    sharpen_strength=sharpen,
                    contrast_alpha=contrast,
                    gamma=gamma,
                    saturation=saturation,
                    upscale_factor=upscale
                )
                
                # Move result to static directory for download
                static_dir = os.path.join(app.root_path, 'static')
                os.makedirs(static_dir, exist_ok=True)
                result_filename = f"enhanced_{filename}"
                final_path = os.path.join(static_dir, result_filename)
                shutil.move(output_path, final_path)
                
                # Cleanup temp directory
                shutil.rmtree(temp_dir, ignore_errors=True)
                
                result_file = result_filename
                
            except Exception as e:
                flash(f'Ошибка при обработке изображения: {str(e)}')
                return redirect(request.url)
        else:
            flash('Неподдерживаемый формат файла')
            return redirect(request.url)
    
    return render_template_string(HTML_TEMPLATE, result_file=result_file)

@app.route('/download/<filename>')
def download_file(filename):
    static_dir = os.path.join(app.root_path, 'static')
    return send_file(os.path.join(static_dir, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)