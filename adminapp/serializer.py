from rest_framework import serializers
from .models import *

class StaffSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ['id', 'user', 'name', 'age', 'gender', 'department']

    def get_name(self, obj):
        return obj.user.name  # Assuming 'user' is the ForeignKey field in the Staff model


class LibrarianSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Librarian
        fields = ['id', 'user' ,'name', 'age', 'gender']

    def get_name(self, obj):
        return obj.user.name  # Assuming 'user' is the ForeignKey field in the Staff model

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','name', 'student_class', 'division', 'gender']

class LibraryHistorySerializer(serializers.ModelSerializer):
    student_id = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    
    class Meta:
        model = LibraryHistory
        fields = ['id', 'book_name', 'student_id' , 'student_name', 'borrow_date', 'return_date', 'status']

    def get_student_id(self, obj):
        return obj.student.id
    
    def get_student_name(self, obj):
        return obj.student.name

class FeeRecordsSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = FeeRecords
        fields = ['id', 'student', 'student_name', 'fee_type', 'amount', 'payment_date', 'remarks']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']  # Include the 'role' field
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        role = validated_data.pop('role', 'staff')  # Default to 'staff' if 'role' is not provided
        user = CustomUser.objects.create_user(**validated_data)
        user.role = role
        user.save()
        return user