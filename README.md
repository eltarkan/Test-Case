# TARKAN CENGIZ TEST CASE

## OVERVIEW

- Aynı karta iki kart sahibi bir kullanıcı ile tek karta sahip kullanıcı nasıl kartını deactivate edecek? İki kart sahibi kartını deactive ederken tek kartlı kullanıcının en az bir aktif kartı olmalı kuralını çiğneyecek.
- Oluşturulan ve herkes tarafından ortak kullanılan kartın ilk sahibi söz hakkına sahip olmalıydı ama bunu ortak tabloda çözmeyi doğru buldum.
- Many2Many için ortak tablo oluşturmaktansa yeni bir tablo oluşturup ekstra deleted_at eklenerek bazı kullanıcılar için kartın silinmesi hedeflendi.
- Ortak değer olan kartların güncellenmesi herkesi etkileyeceği için yeni bir kartın oluşturulması benim nezdimde sağlıklı olan, bu yüzden güncelleme işlemlerinde yeni bir kart sisteme eklendi.
- Transaction işlemlerinde race condition oluşmaması için kuyruklamayı doğru buldum çünkü para yatırma ve çekme işlemlerinin sırası bizim için çok önemli. 
Bu problemi provision ya da RabbitMQ ile çözmenin sağlıklı olacağını düşünüyorum ama bu case'de
RabbitMQ kullanmama sebebim cloud native bir geliştirme planladım ve takvimin gerisine düşmemek için vazgeçtim.
- Postman collection dosyasını ekledim.

## ARCHITECTURE

## HOW TO RUN

- Run
```
  docker-compose up --build
  docker-compose exec app python cli.py migrate
```


## HOW TO BUILD

- Run
```
docker buildx build --platform linux/amd64 --push -t tarkan0110/guardian-api .
```


### CLI Commands
- Run migration
```
alembic upgrade head
```

- Create a migration
```
alembic revision --autogenerate -m "First migration"
```
