from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'patient'
    

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'
    
class IsOwnerOrDoctor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #Patients can only access thier own data
        #doctors can access thier assigned patients data
        if request.user.role =='patient':
           return obj.user ==request.user
        elif request.user.role =='doctor':
            return obj.user.assigned_patients.all()
        return False
        

    