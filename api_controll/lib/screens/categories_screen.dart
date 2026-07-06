import 'package:flutter/material.dart';
import '../services/menu_service.dart';

class CategoriesScreen extends StatefulWidget {
  final int restaurantId;
  CategoriesScreen({required this.restaurantId});

  @override
  _CategoriesScreenState createState() => _CategoriesScreenState();
}

class _CategoriesScreenState extends State<CategoriesScreen> {
  final _service = MenuService();
  bool _isLoading = false;

  void _showAddDialog() {
    final nameCtrl = TextEditingController();
    final descCtrl = TextEditingController();

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Add Category'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: nameCtrl, decoration: InputDecoration(labelText: 'Name')),
              TextField(controller: descCtrl, decoration: InputDecoration(labelText: 'Description')),
            ],
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.of(ctx).pop(), child: Text('Cancel')),
          ElevatedButton(
            onPressed: () async {
              Navigator.of(ctx).pop();
              setState(() => _isLoading = true);
              try {
                await _service.createCategory(
                  restaurantId: widget.restaurantId,
                  name: nameCtrl.text,
                  description: descCtrl.text,
                );
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Category Added!')));
              } catch (e) {
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
              } finally {
                setState(() => _isLoading = false);
              }
            },
            child: Text('Add'),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Manage Categories')),
      body: Center(child: Text('Category list fetching requires GET endpoint implementation.')),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddDialog,
        child: Icon(Icons.add),
      ),
    );
  }
}
