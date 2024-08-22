# Request Logger Module

This Python module is designed to log and store incoming HTTP requests in a Django application. It helps developers track and analyze request data, including headers, methods, and payloads.

## Features
- Log and store HTTP requests.
- Support for GET, POST, PUT, DELETE, and other HTTP methods.
- Ability to filter requests by method or URL.
- Easy integration with Django projects.

## Installation

1. **Install the package via pip:**

    ```bash
    pip install request-logger
    ```

2. **Add `request_logger` to your Django `INSTALLED_APPS`:**

    Open your `settings.py` file and add `request_logger` to the `INSTALLED_APPS` list:

    ```python
    INSTALLED_APPS = [
        # other apps
        'request_logger',
    ]
    ```

3. **Add the Request Logger Middleware:**

    Include the `request_logger` middleware in your `MIDDLEWARE` list in `settings.py`:

    ```python
    MIDDLEWARE = [
        # other middleware
        'request_logger.middleware.request_logger.userLogCheck',
    ]
    ```

4. **Run Migrations to Create the Necessary Database Tables:**

    Apply the migrations to set up the required database tables:

    ```bash
    python manage.py migrate
    ```

## Usage

1. **Filter Logged Requests by Method:**

    You can filter logged requests by method using the following query:

    ```python
    from request_logger.models import userLog

    get_requests = userLog.objects.filter(method='GET')
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# Request Logger Modülü

Bu Python modülü, bir Django uygulamasında gelen HTTP isteklerini kaydetmek ve saklamak için tasarlanmıştır. Geliştiricilere, başlıklar, yöntemler ve payloadlar dahil olmak üzere istek verilerini izleme ve analiz etme imkanı sunar.

## Özellikler
- HTTP isteklerini kaydetme ve saklama.
- GET, POST, PUT, DELETE ve diğer HTTP yöntemleri için destek.
- İstekleri yöntem veya URL'ye göre filtreleme yeteneği.
- Django projeleri ile kolay entegrasyon.

## Kurulum

1. **Pip ile paketi yükleyin:**

    ```bash
    pip install request-logger
    ```

2. **`request_logger` modülünü Django `INSTALLED_APPS` listenize ekleyin:**

    `settings.py` dosyanızı açın ve `INSTALLED_APPS` listesine `request_logger` ekleyin:

    ```python
    INSTALLED_APPS = [
        # diğer uygulamalar
        'request_logger',
    ]
    ```

3. **Request Logger Middleware'ini Ekleyin:**

    `settings.py` dosyanızda `MIDDLEWARE` listesine `request_logger` middleware'ini dahil edin:

    ```python
    MIDDLEWARE = [
        # diğer middleware'ler
        'request_logger.middleware.request_logger.userLogCheck',
    ]
    ```

4. **Gerekli Veritabanı Tablolarını Oluşturmak İçin Migrations İşlemini Çalıştırın:**

    Gerekli veritabanı tablolarını oluşturmak için migrations işlemini uygulayın:

    ```bash
    python manage.py migrate
    ```

## Kullanım


1. **Kaydedilen İstekleri Yönteme Göre Filtreleyin:**

    Kaydedilen istekleri yöntemine göre filtreleyebilirsiniz:

    ```python
    from request_logger.models import userLog

    get_requests = userLog.objects.filter(method='GET')
    ```

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.
