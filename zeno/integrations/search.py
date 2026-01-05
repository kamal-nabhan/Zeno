"""
Image search integration
"""
from icrawler.builtin import GoogleImageCrawler
import os
from typing import Optional


class ImageSearch:
    """Google image search integration"""
    
    def __init__(self, output_dir: str = "./images"):
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """Ensure output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def clear_images(self) -> None:
        """Clear all images from output directory"""
        if not os.path.exists(self.output_dir):
            return
        
        for filename in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {str(e)}")
    
    def search(self, query: str, max_images: int = 1) -> Optional[str]:
        """
        Search for images
        
        Args:
            query: Search query
            max_images: Maximum number of images to download
            
        Returns:
            Error message if failed, None if successful
        """
        try:
            # Clear previous images
            self.clear_images()
            
            # Create crawler and search
            crawler = GoogleImageCrawler(storage={'root_dir': self.output_dir})
            crawler.crawl(keyword=query, max_num=max_images)
            
            return None
        except Exception as e:
            return f"Error searching images: {str(e)}"
