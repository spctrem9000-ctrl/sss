import 'package:flutter/material.dart';
import '../services/menu_service.dart';

class ProductsScreen extends StatefulWidget {
  final int categoryId;
  ProductsScreen({required this.categoryId});

  @override
  _ProductsScreenState createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  final _service = MenuService();
  bool _isLoading = false;

  void _showAddDialog() {
    final nameCtrl = TextEditingController();
    final priceCtrl = TextEditingController();
    final descCtrl = TextEditingController();

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Add Product'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: nameCtrl, decoration: InputDecoration(labelText: 'Product Name')),
              TextField(controller: priceCtrl, decoration: InputDecoration(labelText: 'Base Price'), keyboardType: TextInputType.number),
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
                await _service.createProduct(
                  categoryId: widget.categoryId,
                  name: nameCtrl.text,
                  basePrice: double.parse(priceCtrl.text),
                  description: descCtrl.text,
                );
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Product Added!')));
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
      appBar: AppBar(title: Text('Manage Products')),
      body: Center(child: Text('Product list fetching requires GET endpoint implementation.')),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddDialog,
        child: Icon(Icons.add),
      ),
    );
  }
}
