import 'package:flutter/material.dart';
import 'package:flutter_gemma/flutter_gemma.dart';
import 'screens/setup_screen.dart';
import 'screens/home_screen.dart';
import 'services/gemma_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await FlutterGemma.initialize();
  runApp(const AmmaSewanaApp());
}

class AmmaSewanaApp extends StatelessWidget {
  const AmmaSewanaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Amma Sewana',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF8B1A1A),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      home: const _Launcher(),
    );
  }
}

class _Launcher extends StatefulWidget {
  const _Launcher();

  @override
  State<_Launcher> createState() => _LauncherState();
}

class _LauncherState extends State<_Launcher> {
  bool _checking = true;
  bool _modelReady = false;

  @override
  void initState() {
    super.initState();
    _check();
  }

  Future<void> _check() async {
    final ready = GemmaService().hasActiveModel;
    if (ready) await GemmaService().initialize();
    setState(() {
      _modelReady = ready;
      _checking = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_checking) {
      return const Scaffold(
        backgroundColor: Color(0xFFFFF8F0),
        body: Center(
          child: CircularProgressIndicator(color: Color(0xFF8B1A1A)),
        ),
      );
    }
    return _modelReady ? const HomeScreen() : const SetupScreen();
  }
}
