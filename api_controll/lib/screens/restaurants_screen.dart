import 'package:flutter/material.dart';
import '../models/restaurant.dart';
import '../services/restaurants_service.dart';

class RestaurantsScreen extends StatefulWidget {
  @override
  _RestaurantsScreenState createState() => _RestaurantsScreenState();
}

class _RestaurantsScreenState extends State<RestaurantsScreen> {
  final _service = RestaurantsService();
  List<Restaurant> _restaurants = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadRestaurants();
  }

  Future<void> _loadRestaurants() async {
    setState(() => _isLoading = true);
    try {
      final data = await _service.getRestaurants();
      setState(() => _restaurants = data);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _showAddDialog() {
    final nameCtrl = TextEditingController();
    final slugCtrl = TextEditingController();
    final descCtrl = TextEditingController();

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Add Restaurant'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: nameCtrl, decoration: InputDecoration(labelText: 'Name')),
              TextField(controller: slugCtrl, decoration: InputDecoration(labelText: 'Slug (e.g. kfc-cairo)')),
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
                await _service.createRestaurant(
                  name: nameCtrl.text,
                  slug: slugCtrl.text,
                  description: descCtrl.text,
                );
                _loadRestaurants();
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
      appBar: AppBar(
        title: Text('Restaurants'),
        actions: [
          IconButton(icon: Icon(Icons.refresh), onPressed: _loadRestaurants),
        ],
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : _restaurants.isEmpty
              ? Center(child: Text('No restaurants found.'))
              : ListView.builder(
                  itemCount: _restaurants.length,
                  itemBuilder: (ctx, i) {
                    final r = _restaurants[i];
                    return ListTile(
                      leading: CircleAvatar(child: Icon(Icons.restaurant)),
                      title: Text(r.name),
                      subtitle: Text(r.slug),
                      trailing: Switch(
                        value: r.isActive,
                        onChanged: null, // read-only for now
                      ),
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
