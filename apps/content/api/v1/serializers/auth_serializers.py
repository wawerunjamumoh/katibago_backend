from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from apps.content.models.earned_achievement import EarnedAchievement
from apps.content.models.earned_badge import EarnedBadge
from apps.content.models.learner_profile import LearnerProfile


User = get_user_model()


class EarnedBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarnedBadge
        fields = ("id", "badge_key", "badge_name", "earned_at")
        read_only_fields = fields


class EarnedAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarnedAchievement
        fields = ("id", "achievement_key", "achievement_name", "earned_at")
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = fields


class LearnerProfileSummarySerializer(serializers.ModelSerializer):
    badges = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()

    class Meta:
        model = LearnerProfile
        fields = (
            "id",
            "user",
            "xp",
            "total_xp",
            "current_streak",
            "streak_freeze_count",
            "current_level",
            "gems_balance",
            "badges",
            "achievements",
        )
        read_only_fields = fields

    def get_badges(self, obj):
        return EarnedBadgeSerializer(obj.badges.all(), many=True).data

    def get_achievements(self, obj):
        return EarnedAchievementSerializer(obj.achievements.all(), many=True).data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(trim_whitespace=False)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        attrs["user"] = user
        return attrs

