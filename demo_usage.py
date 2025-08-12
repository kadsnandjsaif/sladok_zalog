#!/usr/bin/env python3
"""
Демонстрация использования ImageEnhancer
"""

from image_enhancer import ImageEnhancer
import os

def demo_enhancement():
    """Демонстрационная функция улучшения изображения"""
    enhancer = ImageEnhancer()
    
    # Пример использования для разных типов изображений
    examples = [
        {
            "name": "Портрет",
            "settings": {
                "denoise_strength": 8,
                "sharpen_strength": 1.1,
                "contrast_alpha": 1.15,
                "gamma": 1.0,
                "saturation": 1.05,
                "upscale_factor": 1.5
            }
        },
        {
            "name": "Пейзаж",
            "settings": {
                "denoise_strength": 12,
                "sharpen_strength": 1.3,
                "contrast_alpha": 1.25,
                "gamma": 1.1,
                "saturation": 1.2,
                "upscale_factor": 2.0
            }
        },
        {
            "name": "Техническое изображение",
            "settings": {
                "denoise_strength": 6,
                "sharpen_strength": 1.8,
                "contrast_alpha": 1.4,
                "gamma": 1.0,
                "saturation": 1.0,
                "upscale_factor": 2.5
            }
        },
        {
            "name": "Старое фото",
            "settings": {
                "denoise_strength": 20,
                "sharpen_strength": 1.0,
                "contrast_alpha": 1.3,
                "gamma": 1.4,
                "saturation": 1.1,
                "upscale_factor": 2.0
            }
        }
    ]
    
    print("🎨 Демонстрация настроек для разных типов изображений:\n")
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['name']}:")
        settings = example['settings']
        print(f"   • Удаление шума: {settings['denoise_strength']}")
        print(f"   • Резкость: {settings['sharpen_strength']}")
        print(f"   • Контрастность: {settings['contrast_alpha']}")
        print(f"   • Гамма: {settings['gamma']}")
        print(f"   • Насыщенность: {settings['saturation']}")
        print(f"   • Увеличение: {settings['upscale_factor']}x")
        print()
    
    print("📝 Пример использования в коде:")
    print("""
from image_enhancer import ImageEnhancer

enhancer = ImageEnhancer()

# Улучшение с пользовательскими настройками
output_path = enhancer.enhance_image_comprehensive(
    'your_image.jpg',
    output_path='enhanced_image.png',
    denoise_strength=10,
    sharpen_strength=1.2,
    contrast_alpha=1.3,
    gamma=1.1,
    saturation=1.15,
    upscale_factor=2.0
)

print(f"Улучшенное изображение сохранено: {output_path}")
""")

def batch_enhance_example():
    """Пример пакетного улучшения изображений"""
    print("📁 Пример пакетного улучшения:")
    print("""
import os
from image_enhancer import ImageEnhancer

def batch_enhance(input_dir, output_dir, **settings):
    enhancer = ImageEnhancer()
    
    # Создаем выходную папку
    os.makedirs(output_dir, exist_ok=True)
    
    # Обрабатываем все изображения в папке
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"enhanced_{filename}")
            
            try:
                enhancer.enhance_image_comprehensive(
                    input_path, 
                    output_path, 
                    **settings
                )
                print(f"✅ Обработан: {filename}")
            except Exception as e:
                print(f"❌ Ошибка при обработке {filename}: {e}")

# Использование
batch_enhance(
    'input_photos/',
    'enhanced_photos/',
    denoise_strength=10,
    sharpen_strength=1.2,
    upscale_factor=2.0
)
""")

if __name__ == "__main__":
    print("🚀 Демонстрация ImageEnhancer\n")
    demo_enhancement()
    print("\n" + "="*60 + "\n")
    batch_enhance_example()