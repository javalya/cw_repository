# ItemLife - 技术方案详细设计

**项目**: 物品寿命App  
**环节**: 3/6 - 技术方案  
**状态**: 📐 详细设计中  
**提交日期**: 2026-03-24

---

## 1. 技术架构总览

### 1.1 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        客户端层 (Flutter)                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Presentation Layer                                  │   │
│  │  ├── screens/ (Home/Add/Detail/Stats/Settings)      │   │
│  │  ├── widgets/ (ItemCard/LifespanBar/CategoryChip)   │   │
│  │  └── providers/ (Riverpod状态管理)                   │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  Domain Layer                                        │   │
│  │  ├── models/ (Item/Category)                         │   │
│  │  ├── repositories/ (抽象接口)                        │   │
│  │  └── services/ (Notification/Analytics)             │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  Data Layer                                          │   │
│  │  ├── local/ (Hive本地存储)                           │   │
│  │  └── remote/ (Firebase远程)                          │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                      本地存储层 (Hive)                       │
│  ├── items_box (物品数据)                                    │
│  ├── settings_box (应用设置)                                 │
│  └── cache_box (临时缓存)                                    │
└──────────────────────────┬──────────────────────────────────┘
                           │ (可选同步)
┌──────────────────────────┴──────────────────────────────────┐
│                    云服务层 (Firebase)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Firestore    │  │ Firebase Auth│  │ Cloud Messaging│    │
│  │ (文档数据库)  │  │ (匿名认证)   │  │ (推送通知)     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术选型理由

| 技术 | 选择 | 理由 |
|------|------|------|
| **Flutter** | ✅ | 一套代码iOS+Android，开发效率高 |
| **Riverpod** | ✅ | 类型安全，性能优，依赖注入方便 |
| **Hive** | ✅ | 本地NoSQL，比SQLite快，支持对象存储 |
| **Firebase** | ✅ | 零运维，免费额度够MVP，实时同步 |
| **Freezed** | ✅ | 代码生成，不可变对象，JSON序列化 |

---

## 2. 数据模型设计

### 2.1 核心模型

```dart
// lib/domain/models/item.dart
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hive/hive.dart';

part 'item.freezed.dart';
part 'item.g.dart';

@HiveType(typeId: 1)
@freezed
class Item with _$Item {
  const factory Item({
    @HiveField(0) required String id,
    @HiveField(1) required String name,
    @HiveField(2) required String category,
    @HiveField(3) required DateTime purchaseDate,
    @HiveField(4) required double price,
    @HiveField(5) required int expectedLifespanMonths,
    @HiveField(6) String? imageUrl,
    @HiveField(7) String? notes,
    @HiveField(8) required DateTime createdAt,
    @HiveField(9) required DateTime updatedAt,
  }) = _Item;

  factory Item.fromJson(Map<String, dynamic> json) => _$ItemFromJson(json);
  
  // 创建新物品工厂方法
  factory Item.create({
    required String name,
    required String category,
    required DateTime purchaseDate,
    required double price,
    required int expectedLifespanMonths,
    String? imageUrl,
    String? notes,
  }) {
    final now = DateTime.now();
    return Item(
      id: const Uuid().v4(),
      name: name,
      category: category,
      purchaseDate: purchaseDate,
      price: price,
      expectedLifespanMonths: expectedLifespanMonths,
      imageUrl: imageUrl,
      notes: notes,
      createdAt: now,
      updatedAt: now,
    );
  }
}

// 扩展方法计算派生属性
extension ItemCalculations on Item {
  // 已使用月数
  int get usedMonths {
    final now = DateTime.now();
    return (now.year - purchaseDate.year) * 12 + 
           (now.month - purchaseDate.month);
  }
  
  // 剩余月数
  int get remainingMonths => expectedLifespanMonths - usedMonths;
  
  // 剩余天数（更精确）
  int get remainingDays {
    final expiryDate = purchaseDate.add(
      Duration(days: expectedLifespanMonths * 30),
    );
    return expiryDate.difference(DateTime.now()).inDays;
  }
  
  // 使用进度百分比 (0-100)
  double get progressPercent {
    if (expectedLifespanMonths == 0) return 0;
    final percent = (usedMonths / expectedLifespanMonths * 100);
    return percent.clamp(0.0, 100.0);
  }
  
  // 日均成本
  double get dailyCost {
    final days = usedMonths * 30;
    if (days <= 0) return price;
    return price / days;
  }
  
  // 预计总成本（使用到预期寿命）
  double get projectedTotalCost {
    return dailyCost * expectedLifespanMonths * 30;
  }
  
  // 状态判断
  bool get isExpiringSoon => remainingMonths <= 1;
  bool get isExpired => remainingMonths <= 0;
  bool get isHealthy => progressPercent < 50;
  bool get isWarning => progressPercent >= 50 && progressPercent < 75;
  bool get isCritical => progressPercent >= 75 && !isExpired;
  
  // 状态颜色
  String get statusColor {
    if (isExpired) return '#E74C3C';
    if (isCritical) return '#F39C12';
    if (isWarning) return '#F1C40F';
    return '#27AE60';
  }
  
  // 状态标签
  String get statusLabel {
    if (isExpired) return '已过期';
    if (isCritical) return '即将到期';
    if (isWarning) return '注意';
    return '正常';
  }
}
```

### 2.2 分类枚举

```dart
// lib/domain/models/category.dart
import 'package:flutter/material.dart';

enum ItemCategory {
  electronics('数码电子', Icons.devices, 'electronics'),
  clothing('衣物鞋帽', Icons.checkroom, 'clothing'),
  furniture('家具家居', Icons.chair, 'furniture'),
  appliances('家用电器', Icons.kitchen, 'appliances'),
  books('图书文具', Icons.book, 'books'),
  sports('运动户外', Icons.sports_basketball, 'sports'),
  beauty('美妆护肤', Icons.face, 'beauty'),
  other('其他', Icons.category, 'other');

  final String label;
  final IconData icon;
  final String key;
  
  const ItemCategory(this.label, this.icon, this.key);
  
  static ItemCategory fromString(String key) {
    return values.firstWhere(
      (c) => c.key == key,
      orElse: () => ItemCategory.other,
    );
  }
}
```

### 2.3 统计模型

```dart
// lib/domain/models/statistics.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'statistics.freezed.dart';

@freezed
class ItemStatistics with _$ItemStatistics {
  const factory ItemStatistics({
    required int totalItems,
    required double totalSpent,
    required double averageDailyCost,
    required Map<String, int> categoryDistribution,
    required Map<String, int> statusDistribution,
    required List<Item> expiringItems,
    required List<MonthlySpending> monthlySpendings,
  }) = _ItemStatistics;
}

@freezed
class MonthlySpending with _$MonthlySpending {
  const factory MonthlySpending({
    required DateTime month,
    required double amount,
    required int itemCount,
  }) = _MonthlySpending;
}
```

---

## 3. 项目结构

```
lib/
├── main.dart
├── app.dart                          # App根组件
├── core/                             # 核心层
│   ├── constants/
│   │   ├── app_constants.dart        # 应用常量
│   │   ├── colors.dart               # 颜色常量
│   │   └── theme.dart                # 主题配置
│   ├── utils/
│   │   ├── date_utils.dart           # 日期工具
│   │   ├── currency_utils.dart       # 货币格式化
│   │   └── validators.dart           # 输入校验
│   └── extensions/
│       ├── date_extension.dart
│       └── string_extension.dart
├── domain/                           # 领域层
│   ├── models/                       # 数据模型
│   │   ├── item.dart
│   │   ├── category.dart
│   │   └── statistics.dart
│   ├── repositories/                 # 仓库接口
│   │   ├── item_repository.dart
│   │   └── settings_repository.dart
│   └── services/                     # 服务接口
│       ├── notification_service.dart
│       └── analytics_service.dart
├── data/                             # 数据层
│   ├── datasources/                  # 数据源
│   │   ├── local/
│   │   │   ├── item_local_source.dart
│   │   │   └── hive_adapters.dart
│   │   └── remote/
│   │       ├── item_remote_source.dart
│   │       └── firebase_config.dart
│   └── repositories/                 # 仓库实现
│       ├── item_repository_impl.dart
│       └── settings_repository_impl.dart
├── presentation/                     # 表现层
│   ├── screens/
│   │   ├── home/
│   │   │   ├── home_screen.dart
│   │   │   └── widgets/
│   │   │       ├── item_list.dart
│   │   │       ├── item_card.dart
│   │   │       └── expiring_section.dart
│   │   ├── add_item/
│   │   │   ├── add_item_screen.dart
│   │   │   └── widgets/
│   │   │       ├── image_picker.dart
│   │   │       └── category_selector.dart
│   │   ├── detail/
│   │   │   ├── item_detail_screen.dart
│   │   │   └── widgets/
│   │   │       ├── lifespan_circle.dart
│   │   │       └── cost_analysis.dart
│   │   ├── stats/
│   │   │   ├── stats_screen.dart
│   │   │   └── widgets/
│   │   │       ├── category_chart.dart
│   │   │       └── spending_chart.dart
│   │   └── settings/
│   │       └── settings_screen.dart
│   ├── widgets/                      # 公共组件
│   │   ├── common/
│   │   │   ├── primary_button.dart
│   │   │   ├── input_field.dart
│   │   │   └── lifespan_bar.dart
│   │   └── feedback/
│   │       ├── loading_indicator.dart
│   │       └── empty_state.dart
│   └── providers/                    # 状态管理
│       ├── item_providers.dart
│       ├── stats_providers.dart
│       └── settings_providers.dart
├── router/                           # 路由
│   └── app_router.dart
└── services/                         # 服务实现
    ├── notification_service_impl.dart
    └── analytics_service_impl.dart
```

---

## 4. 核心功能实现

### 4.1 仓库模式

```dart
// lib/domain/repositories/item_repository.dart
abstract class ItemRepository {
  // CRUD操作
  Future<List<Item>> getAllItems();
  Future<Item?> getItemById(String id);
  Future<void> addItem(Item item);
  Future<void> updateItem(Item item);
  Future<void> deleteItem(String id);
  
  // 查询
  Future<List<Item>> getExpiringItems();
  Future<List<Item>> getItemsByCategory(String category);
  Future<List<Item>> searchItems(String query);
  
  // 实时监听
  Stream<List<Item>> watchAllItems();
  Stream<List<Item>> watchExpiringItems();
  
  // 统计
  Future<ItemStatistics> getStatistics();
}

// lib/data/repositories/item_repository_impl.dart
class ItemRepositoryImpl implements ItemRepository {
  final ItemLocalDataSource _localSource;
  final ItemRemoteDataSource? _remoteSource;
  
  ItemRepositoryImpl(this._localSource, [this._remoteSource]);
  
  @override
  Future<List<Item>> getAllItems() async {
    final items = await _localSource.getAllItems();
    return items..sort((a, b) => a.remainingMonths.compareTo(b.remainingMonths));
  }
  
  @override
  Future<void> addItem(Item item) async {
    await _localSource.addItem(item);
    // 可选：同步到云端
    await _remoteSource?.addItem(item);
  }
  
  @override
  Future<List<Item>> getExpiringItems() async {
    final items = await getAllItems();
    return items.where((item) => item.isExpiringSoon || item.isExpired).toList();
  }
  
  @override
  Stream<List<Item>> watchAllItems() {
    return _localSource.watchAllItems();
  }
  
  @override
  Future<ItemStatistics> getStatistics() async {
    final items = await getAllItems();
    
    // 计算统计数据
    final totalSpent = items.fold(0.0, (sum, item) => sum + item.price);
    final avgDailyCost = items.isEmpty ? 0.0 : 
      items.fold(0.0, (sum, item) => sum + item.dailyCost) / items.length;
    
    // 分类分布
    final categoryDistribution = <String, int>{};
    for (final item in items) {
      categoryDistribution[item.category] = 
        (categoryDistribution[item.category] ?? 0) + 1;
    }
    
    // 状态分布
    final statusDistribution = {
      'healthy': items.where((i) => i.isHealthy).length,
      'warning': items.where((i) => i.isWarning).length,
      'critical': items.where((i) => i.isCritical).length,
      'expired': items.where((i) => i.isExpired).length,
    };
    
    return ItemStatistics(
      totalItems: items.length,
      totalSpent: totalSpent,
      averageDailyCost: avgDailyCost,
      categoryDistribution: categoryDistribution,
      statusDistribution: statusDistribution,
      expiringItems: await getExpiringItems(),
      monthlySpendings: [], // 计算月度消费
    );
  }
  
  // ... 其他方法实现
}
```

### 4.2 状态管理 (Riverpod)

```dart
// lib/presentation/providers/item_providers.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// 仓库Provider
final itemRepositoryProvider = Provider<ItemRepository>((ref) {
  final localSource = ItemLocalDataSourceImpl(Hive.box<Item>('items'));
  return ItemRepositoryImpl(localSource);
});

// 所有物品列表
final itemsProvider = StreamProvider<List<Item>>((ref) {
  final repository = ref.watch(itemRepositoryProvider);
  return repository.watchAllItems();
});

// 即将到期物品
final expiringItemsProvider = FutureProvider<List<Item>>((ref) async {
  final repository = ref.watch(itemRepositoryProvider);
  return repository.getExpiringItems();
});

// 统计信息
final statisticsProvider = FutureProvider<ItemStatistics>((ref) async {
  final repository = ref.watch(itemRepositoryProvider);
  return repository.getStatistics();
});

// 添加物品操作
final addItemProvider = FutureProvider.family<void, ItemFormData>(
  (ref, formData) async {
    final repository = ref.read(itemRepositoryProvider);
    
    final item = Item.create(
      name: formData.name,
      category: formData.category,
      purchaseDate: formData.purchaseDate,
      price: formData.price,
      expectedLifespanMonths: formData.expectedLifespanMonths,
      notes: formData.notes,
    );
    
    await repository.addItem(item);
    
    // 设置提醒
    final notificationService = ref.read(notificationServiceProvider);
    await notificationService.scheduleItemReminder(item);
  },
);

// 表单数据类
class ItemFormData {
  final String name;
  final String category;
  final DateTime purchaseDate;
  final double price;
  final int expectedLifespanMonths;
  final String? notes;
  
  ItemFormData({
    required this.name,
    required this.category,
    required this.purchaseDate,
    required this.price,
    required this.expectedLifespanMonths,
    this.notes,
  });
}
```

### 4.3 本地存储 (Hive)

```dart
// lib/data/datasources/local/hive_adapters.dart
import 'package:hive/hive.dart';
import 'package:itemlife/domain/models/item.dart';

class HiveAdapters {
  static void registerAdapters() {
    Hive.registerAdapter(ItemAdapter());
  }
}

// Hive适配器（由hive_generator生成）
// 运行: flutter packages pub run build_runner build

// lib/data/datasources/local/item_local_source.dart
class ItemLocalDataSourceImpl implements ItemLocalDataSource {
  final Box<Item> _itemBox;
  
  ItemLocalDataSourceImpl(this._itemBox);
  
  @override
  Future<List<Item>> getAllItems() async {
    return _itemBox.values.toList();
  }
  
  @override
  Future<void> addItem(Item item) async {
    await _itemBox.put(item.id, item);
  }
  
  @override
  Future<void> updateItem(Item item) async {
    final updatedItem = item.copyWith(updatedAt: DateTime.now());
    await _itemBox.put(item.id, updatedItem);
  }
  
  @override
  Future<void> deleteItem(String id) async {
    await _itemBox.delete(id);
  }
  
  @override
  Stream<List<Item>> watchAllItems() {
    return _itemBox.watch().map((_) => _itemBox.values.toList());
  }
  
  @override
  Future<void> clearAll() async {
    await _itemBox.clear();
  }
}
```

### 4.4 推送通知

```dart
// lib/services/notification_service_impl.dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/timezone.dart' as tz;

class NotificationServiceImpl implements NotificationService {
  final FlutterLocalNotificationsPlugin _notifications;
  
  NotificationServiceImpl(this._notifications);
  
  @override
  Future<void> initialize() async {
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosSettings = DarwinInitializationSettings();
    
    const initSettings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );
    
    await _notifications.initialize(initSettings);
  }
  
  @override
  Future<void> scheduleItemReminder(Item item) async {
    // 计算提醒时间（到期前7天）
    final reminderDate = item.purchaseDate.add(
      Duration(days: item.expectedLifespanMonths * 30 - 7),
    );
    
    // 如果已经过期，不设置提醒
    if (reminderDate.isBefore(DateTime.now())) return;
    
    await _notifications.zonedSchedule(
      item.id.hashCode, // 唯一ID
      '物品提醒',
      '${item.name} 还有7天就要到预期寿命了',
      tz.TZDateTime.from(reminderDate, tz.local),
      const NotificationDetails(
        android: AndroidNotificationDetails(
          'item_reminders',
          '物品提醒',
          channelDescription: '物品寿命到期提醒',
          importance: Importance.high,
          priority: Priority.high,
        ),
        iOS: DarwinNotificationDetails(
          presentAlert: true,
          presentBadge: true,
          presentSound: true,
        ),
      ),
      androidAllowWhileIdle: true,
      uiLocalNotificationDateInterpretation:
          UILocalNotificationDateInterpretation.absoluteTime,
    );
  }
  
  @override
  Future<void> cancelItemReminder(String itemId) async {
    await _notifications.cancel(itemId.hashCode);
  }
}
```

---

## 5. 依赖配置

```yaml
# pubspec.yaml
name: itemlife
description: 极简物品寿命管理工具

publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # 状态管理
  flutter_riverpod: ^2.4.9
  riverpod_annotation: ^2.3.3
  
  # 本地存储
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # 代码生成
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1
  uuid: ^4.3.3
  
  # 通知
  flutter_local_notifications: ^16.3.2
  timezone: ^0.9.2
  
  # UI组件
  fl_chart: ^0.66.2
  flutter_slidable: ^3.0.1
  image_picker: ^1.0.7
  intl: ^0.19.0
  phosphor_flutter: ^2.0.1
  
  # 工具
  path_provider: ^2.1.2
  share_plus: ^7.2.2
  url_launcher: ^6.2.5
  
  # Firebase（可选，后期添加）
  # firebase_core: ^2.24.2
  # cloud_firestore: ^4.14.0
  # firebase_auth: ^4.16.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
  
  # 代码生成
  build_runner: ^2.4.8
  freezed: ^2.4.6
  json_serializable: ^6.7.1
  hive_generator: ^2.0.1
  riverpod_generator: ^2.3.9
  riverpod_lint: ^2.3.7

flutter:
  uses-material-design: true
  
  assets:
    - assets/images/
```

---

## 6. 性能指标

| 指标 | 目标 | 实现方案 |
|------|------|----------|
| 冷启动时间 | < 2秒 | Flutter引擎优化 + 延迟加载 |
| 列表加载 | < 100ms | Hive本地查询 + 缓存 |
| 添加物品 | < 3秒 | 本地存储 + 后台同步 |
| 内存占用 | < 80MB | 图片懒加载 + 资源释放 |
| 包体积 | < 25MB | 代码混淆 + 资源压缩 |

---

## 7. 安全与隐私

- ✅ **数据本地优先**: 核心数据存储在本地
- ✅ **无需注册**: 匿名使用，保护隐私
- ✅ **数据导出**: 支持CSV导出，用户完全掌控
- ✅ **可选云同步**: 用户主动选择后才上传云端
- ✅ **数据删除**: 支持清空所有数据

---

## 8. 下一步（环节3/6）

**当前环节**: 技术方案详细设计 ✅ 完成  
**下一步**: 开发实现（环节4/6）

**需要确认**:
- [ ] 技术架构方案OK？
- [ ] 数据模型设计OK？
- [ ] 依赖清单OK？
- [ ] 批准进入开发环节？

---

*Tech Architect*  
*2026-03-24*
