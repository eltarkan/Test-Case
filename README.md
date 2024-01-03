# TARKAN CENGIZ TEST CASE

## #OVERVIEW

- Aynı karta iki kart sahibi bir kullanıcı ile tek karta sahip kullanıcı nasıl kartını deactivate edecek? İki kart sahibi kartını deactive ederken tek kartlı kullanıcının en az bir aktif kartı olmalı kuralını çiğneyecek.
- Oluşturulan ve herkes tarafından ortak kullanılan kartın ilk sahibi söz hakkına sahip olmalıydı ama bunu ortak tabloda çözmeyi doğru buldum.
- Many2Many için ortak tablo oluşturmaktansa yeni bir tablo oluşturup ekstra deleted_at eklenerek bazı kullanıcılar için kartın silinmesi hedeflendi.
- Ortak değer olan kartların güncellenmesi herkesi etkileyeceği için yeni bir kartın oluşturulması benim nezdimde sağlıklı olan, bu yüzden güncelleme işlemlerinde yeni bir kart sisteme eklendi.
- Transaction işlemlerinde race condition oluşmaması için kuyruklamayı doğru buldum çünkü para yatırma ve çekme işlemlerinin sırası bizim için çok önemli. 
Bu problemi provision ya da RabbitMQ ile çözmenin sağlıklı olacağını düşündüm ama test case'in dışına çıkmak istemediğim için basit bir kuyruk mekanizması ekledim.
RabbitMQ kullanmama sebebim cloud native bir geliştirme planladım ve takvimin gerisine düşmemek için vazgeçtim.


## #ARCHITECTURE

## #HOW TO RUN

- Create a migration
```
  alembic revision --autogenerate -m "First migration"
```
- Run migration
```
  alembic upgrade head
```
