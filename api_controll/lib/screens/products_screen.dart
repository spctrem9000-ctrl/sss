import 'package:flutter/material.dart';
import '../services/menu_service.dart';
import '../models/product.dart';

class ProductsScreen extends StatefulWidget {
  final int restaurantId;
  final int categoryId;
  final String categoryName;

  ProductsScreen({required this.restaurantId, required this.categoryId, required this.categoryName});

  @override
  _ProductsScreenState createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  final _service = MenuService();
  bool _isLoading = false;
  List<Product> _products = [];

  @override
  void initState() {
    super.initState();
    _fetchProducts();
  }

  Future<void> _fetchProducts() async {
    setState(() => _isLoading = true);
    try {
      final products = await _service.getProducts(widget.categoryId);
      setState(() => _products = products);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _showAddDialog() {
    final nameCtrl = TextEditingController();
    final priceCtrl = TextEditingController();
    final descCtrl = TextEditingController();

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Add Product to ${widget.categoryName}'),
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
                  restaurantId: widget.restaurantId,
                  categoryId: widget.categoryId,
                  name: nameCtrl.text,
                  basePrice: double.parse(priceCtrl.text),
                  description: descCtrl.text,
                );
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Product Added!')));
                _fetchProducts();
              } catch (e) {
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
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
      appBar: AppBar(title: Text('Products in ${widget.categoryName}')),
      body: _isLoading 
        ? Center(child: CircularProgressIndicator())
        : ListView.builder(
            itemCount: _products.length,
            itemBuilder: (ctx, i) {
              final prod = _products[i];
              return ListTile(
                leading: Icon(Icons.fastfood, color: Colors.red),
                title: Text(prod.nameAr),
                subtitle: Text('Price: ${prod.basePrice} SAR'),
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
