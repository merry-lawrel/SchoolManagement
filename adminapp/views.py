from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializer import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Import the permissions at the top of your views.py file
from .permissions import IsAdmin, IsStaff
from rest_framework.permissions import IsAuthenticated,AllowAny  # Make sure the path is correct


def loginAPI(request):
    return render(request, "login.html")

def index(request):
    staffct = Staff.objects.all().count()
    libct = Librarian.objects.all().count()
    studentct = Student.objects.all().count()
    libhisct = LibraryHistory.objects.all().count()
    
    context = {
        'staffct': staffct,
        'libct': libct,
        'studentct': studentct,
        'libhisct': libhisct
    }
    
    return render(request, "index.html", context)

def viewstaff(request):
    staff_list = Staff.objects.all()
    return render(request, 'viewstaff.html', {'staff_list': staff_list})

def addstaff(request):
    return render(request, "addstaff.html")

def viewstudent(request):
    students = Student.objects.all()
    return render(request, 'viewstudent.html', {'students': students})

def addstudent(request):
    return render(request, "addstudent.html")

def viewlibrarians(request):
    librarians = Librarian.objects.all()
    return render(request, "viewlibrarians.html", {'librarians': librarians})

def addlibrarian(request):
    return render(request, "addlibrarian.html")

def libraryhistory(request):
    libhis = LibraryHistory.objects.all()
    return render(request, "libhistory.html", {'library': libhis})

def fee(request):
    fee = FeeRecords.objects.all()
    return render(request, "fee.html", {'fees': fee})


class LoginAPI(APIView):
    template_name = 'login.html'

    def post(self, request):
        username_r = request.POST.get('username')
        password_r = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username_r, password=password_r)
        
        if user is not None:
            # Set session variables based on authenticated user details
            request.session['username'] = username_r
            request.session['role'] = user.role  # Ensure the role is fetched from the user
            request.session['uid'] = user.id

            # Log the user in (this will also create a session for the user)
            login(request, user)
            
            return redirect('index')
        else:
            # If authentication fails, re-render the login page with an error message
            return render(request, self.template_name, {'msg': 'Sorry, invalid credentials.'})

@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPI(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def get(self, request):
        # Clear session variables and log out the user
        request.session.flush()  # Flushes the session data
        return redirect(login)  # Redirect to the homepage or login page  # Redirect to the login page

# View for handling Staff
class StaffAPIView(APIView):

    def get_permissions(self):
        """
        Assign permissions dynamically based on the request method.
        """
        if self.request.method == 'GET':
            # Allow both admin and staff to access the GET method
            permission_classes = [IsAuthenticated, IsAdmin | IsStaff]
        else :
            # Allow only admin to access the POST method
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]

    #@role_required(['admin'])
    def get(self, request, pk=None):
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, pk=None):
        if request.method == 'POST':
            print("Received POST data:", request.data)  # Debug incoming data
            try:
                # Extract user-related data
                user_data = {
                    "name": request.data.get("name"),
                    "username": request.data.get("username"),
                    "password": request.data.get("password"),
                }
                print("User data:", user_data)

                # Validate required fields for CustomUser
                if not all(user_data.values()):
                    return Response({"error": "Name, username, and password are required for CustomUser."},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Create the CustomUser
                custom_user = CustomUser.objects.create_user(
                    username=user_data["username"],
                    password=user_data["password"]
                )
                custom_user.name = user_data["name"]
                custom_user.role = "staff"
                custom_user.save()
                print("CustomUser created:", custom_user)

                # Prepare Staff data (using custom_user.id)
                staff_data = {
                    "user": custom_user.id,
                    "age": request.data.get("age"),
                    "gender": request.data.get("gender"),
                    "department": request.data.get("department"),
                }
                print("Staff data:", staff_data)

                # Serialize and save Staff instance
                serializer = StaffSerializer(data=staff_data)
                if serializer.is_valid():
                    serializer.save()
                    return redirect(viewstaff)
                else:
                    print("Validation errors:", serializer.errors)
                    custom_user.delete()  # Rollback the user creation if Staff validation fails
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                print("Error:", str(e))
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        """Handle POST requests to simulate DELETE"""
        if request.POST.get('_method') == 'DELETE':
                staff = get_object_or_404(Staff, pk=pk)  # Get the staff instance by pk
                staff.delete()  # Delete the staff object from the database
                return redirect(viewstaff)

        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """PUT: Update an existing staff entry"""
        try:
            staff = Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            return Response({"detail": "Staff not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StaffSerializer(staff, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return redirect(viewstaff)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk=None):
    #     """DELETE: Remove a staff entry"""
    #     staff = get_object_or_404(Staff, pk=pk)
    #     staff.delete()
    #     return Response({"detail": "Staff deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Librarian APIView
class LibrarianAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    #@role_required(['admin'])
    def get(self, request, pk=None):
        librarians = Librarian.objects.all()
        serializer = LibrarianSerializer(librarians, many=True)
        return redirect(viewlibrarians)

    #@role_required(['admin'])
    def post(self, request, pk=None):
        """POST: Create a new librarian entry with associated CustomUser"""
        # Extract CustomUser data from the request
        user_data = {
            "name": request.data.get("name"),
            "username": request.data.get("username"),
            "password": request.data.get("password")
        }

        # Validate the presence of required fields
        if not all(user_data.values()):
            return Response({"error": "Name, username, and password are required for CustomUser."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create a new CustomUser instance
        try:
            custom_user = CustomUser.objects.create_user(
                username=user_data["username"],
                password=user_data["password"]
            )
            custom_user.name = user_data["name"]
            custom_user.role = "librarian"  # Assign the 'librarian' role
            custom_user.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare data for Librarian model
        librarian_data = {
            "user": custom_user.id,
            "name": request.data.get("name"),
            "age": request.data.get("age"),
            "gender": request.data.get("gender")
        }

        # Serialize and validate Librarian data
        serializer = LibrarianSerializer(data=librarian_data)
        if serializer.is_valid():
            serializer.save()
            return redirect(viewlibrarians)

        # Rollback CustomUser creation if Librarian data is invalid
        custom_user.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@role_required(['admin'])
    def put(self, request, pk=None):
        """Handle PUT requests to update librarian details."""
        librarian = get_object_or_404(Librarian, pk=pk)
        serializer = LibrarianSerializer(librarian, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect('view_librarians')  # Redirect to the librarian list page
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@role_required(['admin'])
    def delete(self, request, pk):
        """DELETE: Remove a librarian entry"""
        librarian = get_object_or_404(Librarian, pk=pk)
        librarian.delete()
        return Response({"message": "Librarian deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


#@method_decorator(role_required(['admin', 'staff']), name='dispatch')
class StudentAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk=None):
        if pk:
            try:
                student = Student.objects.get(pk=pk)
                serializer = StudentSerializer(student)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Student.DoesNotExist:
                return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect(viewstudent)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        """Handle POST requests to simulate DELETE"""
        if request.POST.get('_method') == 'DELETE':
            student = get_object_or_404(Student, pk=pk)  # Get the staff instance by pk
            student.delete()  # Delete the staff object from the database
            return redirect(viewstudent)
        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LibraryHistoryAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    #@role_required(['admin', 'librarian', 'staff'])
    def get(self, request, pk=None):
        if pk:
            try:
                history = LibraryHistory.objects.get(pk=pk)
                serializer = LibraryHistorySerializer(history)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except LibraryHistory.DoesNotExist:
                return Response({"detail": "Library history not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            histories = LibraryHistory.objects.all()
            serializer = LibraryHistorySerializer(histories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    #@role_required(['admin', 'librarian'])
    def post(self, request):
        serializer = LibraryHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@role_required(['admin'])
    def put(self, request, pk=None):
        try:
            history = LibraryHistory.objects.get(pk=pk)
        except LibraryHistory.DoesNotExist:
            return Response({"detail": "Library history not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LibraryHistorySerializer(history, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@role_required(['admin'])
    def patch(self, request, pk=None):
        try:
            history = LibraryHistory.objects.get(pk=pk)
        except LibraryHistory.DoesNotExist:
            return Response({"detail": "Library history not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LibraryHistorySerializer(history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@role_required(['admin'])
    def delete(self, request, pk=None):
        try:
            history = LibraryHistory.objects.get(pk=pk)
            history.delete()
            return Response({"detail": "Library history deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except LibraryHistory.DoesNotExist:
            return Response({"detail": "Library history not found."}, status=status.HTTP_404_NOT_FOUND)

class FeeRecordsAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    #@role_required(['admin', 'staff'])
    def get(self, request, pk=None):
        if pk:
            try:
                fee_record = FeeRecords.objects.get(pk=pk)
                serializer = FeeRecordsSerializer(fee_record)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except FeeRecords.DoesNotExist:
                return Response({"detail": "Fee record not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            fee_records = FeeRecords.objects.all()
            serializer = FeeRecordsSerializer(fee_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    #@role_required(['admin', 'staff'])
    def post(self, request):
        serializer = FeeRecordsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@role_required(['admin', 'staff'])
    def put(self, request, pk=None):
        try:
            fee_record = FeeRecords.objects.get(pk=pk)
        except FeeRecords.DoesNotExist:
            return Response({"detail": "Fee record not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FeeRecordsSerializer(fee_record, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@role_required(['admin', 'staff'])
    def patch(self, request, pk=None):
        try:
            fee_record = FeeRecords.objects.get(pk=pk)
        except FeeRecords.DoesNotExist:
            return Response({"detail": "Fee record not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FeeRecordsSerializer(fee_record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@role_required(['admin', 'staff'])
    def delete(self, request, pk=None):
        try:
            fee_record = FeeRecords.objects.get(pk=pk)
            fee_record.delete()
            return Response({"detail": "Fee record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except FeeRecords.DoesNotExist:
            return Response({"detail": "Fee record not found."}, status=status.HTTP_404_NOT_FOUND)

