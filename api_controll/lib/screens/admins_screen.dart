import 'package:flutter/material.dart';
import '../services/api_client.dart';
import '../models/restaurant.dart';
import '../services/restaurants_service.dart';

class AdminsScreen extends StatefulWidget {
  @override
  _AdminsScreenState createState() => _AdminsScreenState();
}

class _AdminsScreenState extends State<AdminsScreen> {
  final _api = ApiClient();
  final _restService = RestaurantsService();
  
  bool _isLoading = true;
  List<dynamic> _admins = [];
  List<Restaurant> _restaurants = [];

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    try {
      final res = await _api.get('/admin/users');
      final rests = await _restService.getRestaurants();
      setState(() {
        _admins = res is List ? res : [];
        _restaurants = rests;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _showAddDialog() {
    final emailCtrl = TextEditingController();
    final passCtrl = TextEditingController();
    final firstCtrl = TextEditingController();
    final lastCtrl = TextEditingController();
    int? selectedRestId;

    showDialog(
      context: context,
      builder: (ctx) => StatefulBuilder(
        builder: (context, setStateSB) => AlertDialog(
          title: Text('Add Restaurant Owner'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(controller: emailCtrl, decoration: InputDecoration(labelText: 'Email')),
                TextField(controller: passCtrl, decoration: InputDecoration(labelText: 'Password'), obscureText: true),
                TextField(controller: firstCtrl, decoration: InputDecoration(labelText: 'First Name')),
                TextField(controller: lastCtrl, decoration: InputDecoration(labelText: 'Last Name')),
                SizedBox(height: 16),
                DropdownButtonFormField<int>(
                  decoration: InputDecoration(labelText: 'Select Restaurant'),
                  items: _restaurants.map((r) => DropdownMenuItem(
                    value: r.id,
                    child: Text(r.name),
                  )).toList(),
                  onChanged: (val) => setStateSB(() => selectedRestId = val),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(onPressed: () => Navigator.of(ctx).pop(), child: Text('Cancel')),
            ElevatedButton(
              onPressed: () async {
                if (selectedRestId == null) {
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Please select a restaurant')));
                  return;
                }
                Navigator.of(ctx).pop();
                setState(() => _isLoading = true);
                try {
                  await _api.post('/admin/users', {
                    'email': emailCtrl.text,
                    'password': passCtrl.text,
                    'first_name': firstCtrl.text,
                    'last_name': lastCtrl.text,
                    'restaurant_id': selectedRestId,
                  });
                  _loadData();
                } catch (e) {
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
                  setState(() => _isLoading = false);
                }
              },
              child: Text('Add Owner'),
            )
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Manage Owners')),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : _admins.isEmpty
              ? Center(child: Text('No owners found.'))
              : ListView.builder(
                  itemCount: _admins.length,
                  itemBuilder: (ctx, i) {
                    final a = _admins[i];
                    return ListTile(
                      leading: CircleAvatar(child: Icon(Icons.person)),
                      title: Text('${a["first_name"]} ${a["last_name"]}'),
                      subtitle: Text('${a["email"]} - Rest ID: ${a["restaurant_id"]}'),
                    );
                  },
                ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddDialog,
        child: Icon(Icons.add),
      ),
    );
  }
}
