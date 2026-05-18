import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/gemma_service.dart';
import 'home_screen.dart';

class SetupScreen extends StatefulWidget {
  const SetupScreen({super.key});

  @override
  State<SetupScreen> createState() => _SetupScreenState();
}

class _SetupScreenState extends State<SetupScreen> {
  int _progress = 0;
  bool _downloading = false;
  String? _error;

  Future<void> _startDownload() async {
    setState(() {
      _downloading = true;
      _error = null;
    });
    try {
      await GemmaService().downloadModel(
        onProgress: (p) => setState(() => _progress = p),
      );
      await GemmaService().initialize();
      if (mounted) {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (_) => const HomeScreen()),
        );
      }
    } catch (e) {
      setState(() {
        _downloading = false;
        _error = 'Download failed. Check your internet connection and try again.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFF8F0),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 40),
              Text(
                'මාතෘ සේවා',
                style: GoogleFonts.notoSansSinhala(
                  fontSize: 36,
                  fontWeight: FontWeight.bold,
                  color: const Color(0xFF8B1A1A),
                ),
              ),
              Text(
                'Amma Sewana',
                style: GoogleFonts.poppins(fontSize: 20, color: Colors.grey[600]),
              ),
              const SizedBox(height: 6),
              Text(
                'AI Midwife Assistant · PHM සහායකයා',
                style: GoogleFonts.poppins(fontSize: 13, color: Colors.grey[500]),
              ),
              const Spacer(),
              Card(
                elevation: 2,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.download_rounded,
                              color: Color(0xFF8B1A1A), size: 28),
                          const SizedBox(width: 12),
                          Text(
                            'One-time setup',
                            style: GoogleFonts.poppins(
                                fontWeight: FontWeight.w600, fontSize: 18),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Text(
                        'Download Gemma 4 AI model (~2.6GB) over WiFi. After this, the app works fully offline — no internet needed.',
                        style: GoogleFonts.poppins(
                            fontSize: 14, color: Colors.grey[600], height: 1.5),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          const Icon(Icons.wifi_off,
                              size: 16, color: Color(0xFF2E7D32)),
                          const SizedBox(width: 6),
                          Text(
                            'Works offline forever after download',
                            style: GoogleFonts.poppins(
                                fontSize: 12,
                                color: const Color(0xFF2E7D32),
                                fontWeight: FontWeight.w500),
                          ),
                        ],
                      ),
                      if (_error != null) ...[
                        const SizedBox(height: 12),
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: Colors.red[50],
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(_error!,
                              style: TextStyle(
                                  color: Colors.red[700], fontSize: 12)),
                        ),
                      ],
                      const SizedBox(height: 24),
                      if (_downloading) ...[
                        ClipRRect(
                          borderRadius: BorderRadius.circular(4),
                          child: LinearProgressIndicator(
                            value: _progress / 100,
                            backgroundColor: Colors.grey[200],
                            color: const Color(0xFF8B1A1A),
                            minHeight: 8,
                          ),
                        ),
                        const SizedBox(height: 10),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              '$_progress% downloaded',
                              style: GoogleFonts.poppins(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w500,
                                  color: const Color(0xFF8B1A1A)),
                            ),
                            Text(
                              'Keep app open',
                              style: GoogleFonts.poppins(
                                  fontSize: 12, color: Colors.grey[500]),
                            ),
                          ],
                        ),
                      ] else
                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton.icon(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0xFF8B1A1A),
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12)),
                            ),
                            onPressed: _startDownload,
                            icon: const Icon(Icons.download_rounded),
                            label: Text(
                              'Download Gemma 4 & Start',
                              style: GoogleFonts.poppins(
                                  fontWeight: FontWeight.w600, fontSize: 15),
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
              ),
              const Spacer(),
            ],
          ),
        ),
      ),
    );
  }
}
