import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncClient

load_dotenv()

async def create_vector_store():
    """Создает векторное хранилище в OpenAI и возвращает его ID."""
    # Используем API ключ из переменной окружения или передаем напрямую
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Ошибка: Установите переменную окружения OPENAI_API_KEY")
        return
    
    client = AsyncClient(api_key=api_key)
    
    try:
        # Создать векторное хранилище (используем vector_stores напрямую, не через beta)
        # Метод create принимает только name, без description
        vector_store = await client.vector_stores.create(
            name="Coach Agent Vector Store"
        )
        
        print(f"✅ Векторное хранилище успешно создано!")
        print(f"VS_ID: {vector_store.id}")
        print(f"\nДобавьте это в ваш .env файл:")
        print(f"VS_ID={vector_store.id}")
        
        return vector_store.id
    except Exception as e:
        print(f"❌ Ошибка при создании векторного хранилища: {e}")
        print("\nАльтернативный способ - создайте векторное хранилище через веб-интерфейс OpenAI:")
        print("https://platform.openai.com/playground")
        return None

if __name__ == "__main__":
    asyncio.run(create_vector_store())