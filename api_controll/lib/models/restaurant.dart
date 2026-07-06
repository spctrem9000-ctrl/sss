class Restaurant {
  final int id;
  final String name;
  final String slug;
  final String description;
  final bool isActive;
  final String? logoUrl;
  final String? coverUrl;
  final String? contactEmail;
  final String? contactPhone;
  final String? address;

  Restaurant({
    required this.id,
    required this.name,
    required this.slug,
    required this.description,
    required this.isActive,
    this.logoUrl,
    this.coverUrl,
    this.contactEmail,
    this.contactPhone,
    this.address,
  });

  factory Restaurant.fromJson(Map<String, dynamic> json) {
    return Restaurant(
      id: json['id'],
      name: json['name'],
      slug: json['slug'],
      description: json['description'] ?? '',
      isActive: json['is_active'] ?? true,
      logoUrl: json['logo_url'],
      coverUrl: json['cover_url'],
      contactEmail: json['contact_email'],
      contactPhone: json['contact_phone'],
      address: json['address'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'slug': slug,
      'description': description,
      'is_active': isActive,
      'logo_url': logoUrl,
      'cover_url': coverUrl,
      'contact_email': contactEmail,
      'contact_phone': contactPhone,
      'address': address,
    };
  }
}
