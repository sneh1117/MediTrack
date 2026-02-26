from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'patient'
    

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'
    
class IsOwnerOrDoctor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #Blocks unautheticated user immediately
        if not request.user.is_authenticated:
            return False
        
        obj_user= getattr(obj,'user',None)
        if obj_user is None:
            return False
        
        #Patients can only access their own data 

        if request.user.role=='patient':
            return obj_user == request.user
        
        #Doctors can only access their ASSIGNED patient's data

        elif request.user.role=='doctor':
            return obj_user in request.user.assigned_patients.all()
        
        return False
        

    