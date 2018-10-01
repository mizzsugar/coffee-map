from django.core.management.base import BaseCommand
import minsta.models
import minsta.domain

# TODO: cronに設定する
class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Delete the expired record in ForgetPasswordUer table'


    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        minsta.domain.expire_frogetpassworduser()
        