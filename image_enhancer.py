#!/usr/bin/env python3
"""
Image Quality Enhancement Tool
Улучшает качество изображений с помощью различных фильтров и техник
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import argparse
import os
import sys

class ImageEnhancer:
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    
    def load_image(self, image_path):
        """Загрузка изображения"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Файл не найден: {image_path}")
        
        # Проверка формата
        ext = os.path.splitext(image_path)[1].lower()
        if ext not in self.supported_formats:
            raise ValueError(f"Неподдерживаемый формат: {ext}")
        
        # Загрузка с помощью PIL
        pil_image = Image.open(image_path).convert('RGB')
        # Конвертация в OpenCV формат
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return pil_image, cv_image
    
    def denoise_image(self, cv_image, strength=10):
        """Удаление шума"""
        return cv2.fastNlMeansDenoisingColored(cv_image, None, strength, strength, 7, 21)
    
    def sharpen_image(self, cv_image, strength=1.5):
        """Повышение резкости"""
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        sharpened = cv2.filter2D(cv_image, -1, kernel)
        return cv2.addWeighted(cv_image, 1-strength+1, sharpened, strength, 0)
    
    def enhance_contrast(self, cv_image, alpha=1.3, beta=10):
        """Улучшение контрастности и яркости"""
        return cv2.convertScaleAbs(cv_image, alpha=alpha, beta=beta)
    
    def adjust_gamma(self, cv_image, gamma=1.2):
        """Гамма-коррекция"""
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(cv_image, table)
    
    def enhance_colors(self, pil_image, saturation=1.2, vibrance=1.1):
        """Улучшение цветов"""
        # Увеличение насыщенности
        enhancer = ImageEnhance.Color(pil_image)
        enhanced = enhancer.enhance(saturation)
        
        # Дополнительное улучшение через HSV
        cv_image = cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:,:,1] *= vibrance  # Увеличение насыщенности
        hsv[:,:,1] = np.clip(hsv[:,:,1], 0, 255)
        
        enhanced_cv = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        return Image.fromarray(cv2.cvtColor(enhanced_cv, cv2.COLOR_BGR2RGB))
    
    def upscale_image(self, cv_image, scale_factor=2):
        """Увеличение разрешения с помощью EDSR"""
        height, width = cv_image.shape[:2]
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        # Используем INTER_CUBIC для лучшего качества
        upscaled = cv2.resize(cv_image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        return upscaled
    
    def apply_unsharp_mask(self, cv_image, sigma=1.0, strength=1.5, threshold=0):
        """Применение Unsharp Mask для улучшения деталей"""
        blurred = cv2.GaussianBlur(cv_image, (0, 0), sigma)
        sharpened = cv2.addWeighted(cv_image, 1.0 + strength, blurred, -strength, threshold)
        return sharpened
    
    def enhance_image_comprehensive(self, image_path, output_path=None, 
                                  denoise_strength=10, sharpen_strength=1.2,
                                  contrast_alpha=1.2, gamma=1.1, 
                                  saturation=1.15, upscale_factor=1.5):
        """Комплексное улучшение изображения"""
        print(f"Загрузка изображения: {image_path}")
        pil_image, cv_image = self.load_image(image_path)
        
        print("Применение фильтров...")
        
        # 1. Удаление шума
        print("- Удаление шума...")
        cv_image = self.denoise_image(cv_image, denoise_strength)
        
        # 2. Увеличение разрешения
        if upscale_factor > 1:
            print(f"- Увеличение разрешения в {upscale_factor}x...")
            cv_image = self.upscale_image(cv_image, upscale_factor)
        
        # 3. Улучшение контрастности
        print("- Улучшение контрастности...")
        cv_image = self.enhance_contrast(cv_image, contrast_alpha)
        
        # 4. Гамма-коррекция
        print("- Гамма-коррекция...")
        cv_image = self.adjust_gamma(cv_image, gamma)
        
        # 5. Повышение резкости с Unsharp Mask
        print("- Повышение резкости...")
        cv_image = self.apply_unsharp_mask(cv_image, strength=sharpen_strength)
        
        # 6. Улучшение цветов
        print("- Улучшение цветов...")
        pil_result = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        pil_result = self.enhance_colors(pil_result, saturation)
        
        # Определение выходного файла
        if output_path is None:
            base_name = os.path.splitext(image_path)[0]
            output_path = f"{base_name}_enhanced.png"
        
        # Сохранение результата
        print(f"Сохранение результата: {output_path}")
        pil_result.save(output_path, quality=95, optimize=True)
        
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Улучшение качества изображений')
    parser.add_argument('input_image', help='Путь к входному изображению')
    parser.add_argument('-o', '--output', help='Путь к выходному файлу')
    parser.add_argument('--denoise', type=int, default=10, help='Сила удаления шума (0-30)')
    parser.add_argument('--sharpen', type=float, default=1.2, help='Сила повышения резкости (0.5-3.0)')
    parser.add_argument('--contrast', type=float, default=1.2, help='Улучшение контрастности (0.5-3.0)')
    parser.add_argument('--gamma', type=float, default=1.1, help='Гамма-коррекция (0.5-2.0)')
    parser.add_argument('--saturation', type=float, default=1.15, help='Насыщенность цветов (0.5-2.0)')
    parser.add_argument('--upscale', type=float, default=1.5, help='Коэффициент увеличения (1.0-4.0)')
    
    args = parser.parse_args()
    
    enhancer = ImageEnhancer()
    
    try:
        output_path = enhancer.enhance_image_comprehensive(
            args.input_image,
            args.output,
            args.denoise,
            args.sharpen,
            args.contrast,
            args.gamma,
            args.saturation,
            args.upscale
        )
        print(f"\n✅ Улучшение завершено!")
        print(f"📁 Результат сохранен: {output_path}")
        
        # Показать информацию о размерах
        original = Image.open(args.input_image)
        enhanced = Image.open(output_path)
        print(f"📊 Размер оригинала: {original.size}")
        print(f"📊 Размер улучшенного: {enhanced.size}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()