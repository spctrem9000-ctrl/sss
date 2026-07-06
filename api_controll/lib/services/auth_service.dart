import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/admin_user.dart';
import 'api_client.dart';

class AuthService {
  final ApiClient _api = ApiClient();

  Future<AdminUser> login(String email, String password) async {
    final response = await _api.post('/admin/auth/login', {
      'email': email,
      'password': password,
    });
    
    final token = response['access_token'];
    final adminJson = response['admin'];
    
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
    await prefs.setString('admin_data', jsonEncode(adminJson));
    
    return AdminUser.fromJson(adminJson);
  }

  Future<AdminUser> setupSuperAdmin(String email, String password) async {
    final response = await _api.post('/admin/auth/setup', {
      'email': email,
      'password': password,
    });
    
    final token = response['access_token'];
    final adminJson = response['admin'];
    
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
    await prefs.setString('admin_data', jsonEncode(adminJson));
    
    return AdminUser.fromJson(adminJson);
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    await prefs.remove('admin_data');
  }

  Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.containsKey('access_token');
  }
}
