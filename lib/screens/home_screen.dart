import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/patient.dart';
import '../widgets/risk_badge.dart';
import 'visit_screen.dart';
import 'chat_screen.dart';

// Demo patients — replace with real DB in production
final _demoPatients = [
  Patient(
    id: '1',
    name: 'Kamala Perera',
    nameSinhala: 'කමලා පේරේරා',
    village: 'Negombo',
    weeksPregnant: 32,
    riskLevel: RiskLevel.high,
    lastVisit: DateTime.now().subtract(const Duration(days: 7)),
  ),
  Patient(
    id: '2',
    name: 'Priya Rajendran',
    nameSinhala: 'பிரியா ராஜேந்திரன்',
    village: 'Colombo 5',
    weeksPregnant: 20,
    riskLevel: RiskLevel.low,
    lastVisit: DateTime.now().subtract(const Duration(days: 14)),
  ),
  Patient(
    id: '3',
    name: 'Sunethra Bandara',
    nameSinhala: 'සුනේත්‍රා බණ්ඩාර',
    village: 'Kandy',
    weeksPregnant: 36,
    riskLevel: RiskLevel.urgent,
    lastVisit: DateTime.now().subtract(const Duration(days: 2)),
  ),
  Patient(
    id: '4',
    name: 'Nadeeka Silva',
    nameSinhala: 'නදීකා සිල්වා',
    village: 'Gampaha',
    weeksPregnant: 28,
    riskLevel: RiskLevel.medium,
    lastVisit: DateTime.now().subtract(const Duration(days: 10)),
  ),
];

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String _language = 'sinhala';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFF8F0),
      appBar: AppBar(
        backgroundColor: const Color(0xFF8B1A1A),
        foregroundColor: Colors.white,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'මාතෘ සේවා',
              style: GoogleFonts.notoSansSinhala(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              'PHM Midwife Assistant',
              style: GoogleFonts.poppins(fontSize: 11),
            ),
          ],
        ),
        actions: [
          _LanguageToggle(
            current: _language,
            onChanged: (lang) => setState(() => _language = lang),
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildAskGemmaBar(),
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: Text(
              'ගෙදර රෝගීන් · My Mothers',
              style: GoogleFonts.notoSansSinhala(
                fontSize: 15,
                fontWeight: FontWeight.w600,
                color: Colors.grey[700],
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 12),
              itemCount: _demoPatients.length,
              itemBuilder: (ctx, i) =>
                  _PatientCard(patient: _demoPatients[i], language: _language),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAskGemmaBar() {
    return GestureDetector(
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ChatScreen(language: _language),
        ),
      ),
      child: Container(
        margin: const EdgeInsets.fromLTRB(12, 12, 12, 0),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(
          color: Colors.white,
          border: Border.all(color: const Color(0xFF8B1A1A), width: 1.5),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            const Icon(Icons.psychology_outlined, color: Color(0xFF8B1A1A)),
            const SizedBox(width: 12),
            Text(
              'Gemma ගෙන් අසන්න · Ask Gemma',
              style: GoogleFonts.poppins(
                fontSize: 14,
                color: const Color(0xFF8B1A1A),
              ),
            ),
            const Spacer(),
            const Icon(Icons.arrow_forward_ios,
                size: 14, color: Color(0xFF8B1A1A)),
          ],
        ),
      ),
    );
  }
}

class _PatientCard extends StatelessWidget {
  final Patient patient;
  final String language;
  const _PatientCard({required this.patient, required this.language});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      elevation: patient.riskLevel == RiskLevel.urgent ? 4 : 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: patient.riskLevel == RiskLevel.urgent
            ? const BorderSide(color: Color(0xFFD32F2F), width: 2)
            : BorderSide.none,
      ),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => VisitScreen(patient: patient, language: language),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Row(
            children: [
              CircleAvatar(
                backgroundColor: _avatarColor(patient.riskLevel),
                child: Text(
                  patient.name[0],
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      language == 'english' ? patient.name : patient.nameSinhala,
                      style: GoogleFonts.poppins(
                        fontWeight: FontWeight.w600,
                        fontSize: 14,
                      ),
                    ),
                    Text(
                      '${patient.village} · ${patient.weeksPregnant}w',
                      style: GoogleFonts.poppins(
                          fontSize: 12, color: Colors.grey[500]),
                    ),
                  ],
                ),
              ),
              RiskBadge(level: patient.riskLevel),
            ],
          ),
        ),
      ),
    );
  }

  Color _avatarColor(RiskLevel level) => switch (level) {
        RiskLevel.urgent => const Color(0xFFD32F2F),
        RiskLevel.high => const Color(0xFFE65100),
        RiskLevel.medium => const Color(0xFFF9A825),
        RiskLevel.low => const Color(0xFF2E7D32),
      };
}

class _LanguageToggle extends StatelessWidget {
  final String current;
  final void Function(String) onChanged;
  const _LanguageToggle({required this.current, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    final labels = {'sinhala': 'සිං', 'tamil': 'தமி', 'english': 'EN'};
    final next = switch (current) {
      'sinhala' => 'tamil',
      'tamil' => 'english',
      _ => 'sinhala',
    };
    return TextButton(
      onPressed: () => onChanged(next),
      child: Text(
        labels[current]!,
        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
      ),
    );
  }
}
