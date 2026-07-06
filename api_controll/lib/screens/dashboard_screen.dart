import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'login_screen.dart';
import 'restaurants_screen.dart';
import 'categories_screen.dart';
import 'products_screen.dart';
import 'admins_screen.dart';

class DashboardScreen extends StatelessWidget {
  final _authService = AuthService();

  void _logout(BuildContext context) async {
    await _authService.logout();
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => LoginScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Admin Dashboard'),
        actions: [
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: () => _logout(context),
          )
        ],
      ),
      body: GridView.count(
        crossAxisCount: 2,
        padding: EdgeInsets.all(16),
        mainAxisSpacing: 16,
        crossAxisSpacing: 16,
        children: [
          _buildCard(
            context,
            'Restaurants',
            Icons.restaurant,
            Colors.orange,
            () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => RestaurantsScreen()),
            ),
          ),
          _buildCard(context, 'Owners/Admins', Icons.admin_panel_settings, Colors.blue, () {
            Navigator.of(context).push(MaterialPageRoute(builder: (_) => AdminsScreen()));
          }),
          _buildCard(context, 'Orders', Icons.receipt, Colors.purple, () {}),
          _buildCard(context, 'Settings', Icons.settings, Colors.grey, () {}),
        ],
      ),
    );
  }

  Widget _buildCard(BuildContext context, String title, IconData icon, Color color, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      child: Card(
        elevation: 4,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 48, color: color),
            SizedBox(height: 16),
            Text(title, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }
}
