import jwt

from datetime import datetime, timedelta

from django.conf import settings 

from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
)

from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        # Создает пользователя с email, паролем и именем
        if username is None:
            raise TypeError('User must have a username.')

        if email is None:
            raise TypeError('User must have an email address.')
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, email, password):
        # Создает и возвращает суперпользователя
        if password is None:
            raise TypeError('Superuser must have a password')
        
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(db_index=True, max_length=255, uniaue=True)

    email = models.EmailField(db_index=True, unique=True)
    # "Мягкое" удаление - учетная запись пользователя деактивируется
    is_active = models.BooleanField(default=True)
    # Принадлежность к группе администраторов
    is_staff = models.BooleanField(default=False)
    # Временная метка создания объекта
    created_at = models.DateTimeField(auto_now_add = True)
    # Временная метка обновления объекта
    updated_at = models.DateTimeField(auto_now=True)

    # Указывает на поле, используемое для авторизации пользователя
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Указывает, что класс UserManager 
    # должен использоваться для управления объектами User
    objects = UserManager()

    def __str__(self):
        ''' Строковое представление в консоли'''
        return self.email
    
    @property
    def token(self):
        ''' 
        Метод генерирует JSON веб-токен с помощью 
        user._generate_jwt_token()
        '''
        return self._generate_jwt_token()
    
    def get_full_name(self):
        '''
        Метод возвращает имя пользователя
        '''
        return self.username
    
    def get_short_name(self):
        '''
        Метод возвращает имя пользователя
        '''
        return self.username
    
    def _generate_jwt_token(self):
        '''
        Метод генерирует JSON веб-токен, который 
        хранится в браузере пользователя. 
        Срок действия токена 1 день.
        '''

        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id' : self.pk,
            'exp' : int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')






