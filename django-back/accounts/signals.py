from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from .models import User
from .embedding_utils import update_user_embedding

@receiver(m2m_changed, sender=User.interested_categories.through)
def update_user_embedding_on_categories_change(sender, instance, action, **kwargs):
    """관심 카테고리가 변경될 때 사용자 임베딩 업데이트"""
    if action in ["post_add", "post_remove", "post_clear"]:
        # 최근에 임베딩이 업데이트되지 않은 경우에만 실행
        if not instance.embedding_updated_at or (timezone.now() - instance.embedding_updated_at).seconds > 5:
            update_user_embedding(instance)

# 북마크 관련 시그널은 제거하고 book_like 뷰에서 직접 처리

@receiver(post_save, sender=User)
def update_user_embedding_on_profile_change(sender, instance, created, **kwargs):
    """사용자 프로필(자기소개 등)이 변경될 때 임베딩 업데이트"""
    if not created and not kwargs.get('raw', False):  # 새로운 사용자 생성이 아닌 경우에만
        # bio 필드가 변경되었고, 임베딩 업데이트로 인한 저장이 아닌 경우에만
        if instance.tracker.has_changed('bio') and not instance.tracker.has_changed('embedding_vector'):
            update_user_embedding(instance)
