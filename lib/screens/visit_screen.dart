import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/patient.dart';
import '../services/gemma_service.dart';
import '../widgets/risk_badge.dart';

class VisitScreen extends StatefulWidget {
  final Patient patient;
  final String language;
  const VisitScreen({super.key, required this.patient, required this.language});

  @override
  State<VisitScreen> createState() => _VisitScreenState();
}

class _VisitScreenState extends State<VisitScreen> {
  final _systolicCtrl = TextEditingController();
  final _diastolicCtrl = TextEditingController();
  final _hbCtrl = TextEditingController();
  final _fundalCtrl = TextEditingController();
  bool _hasOedema = false;
  bool _loading = false;
  String? _assessment;
  RiskLevel? _detectedRisk;

  @override
  void dispose() {
    _systolicCtrl.dispose();
    _diastolicCtrl.dispose();
    _hbCtrl.dispose();
    _fundalCtrl.dispose();
    super.dispose();
  }

  RiskLevel _quickRisk() {
    final sys = int.tryParse(_systolicCtrl.text) ?? 0;
    final dia = int.tryParse(_diastolicCtrl.text) ?? 0;
    final hb = double.tryParse(_hbCtrl.text) ?? 11.0;
    if (sys >= 160 || dia >= 100 || hb < 8.0) return RiskLevel.urgent;
    if (sys >= 140 || dia >= 90 || hb < 9.0 || _hasOedema) return RiskLevel.high;
    if (hb < 11.0) return RiskLevel.medium;
    return RiskLevel.low;
  }

  Future<void> _assess() async {
    final sys = int.tryParse(_systolicCtrl.text);
    final dia = int.tryParse(_diastolicCtrl.text);
    final hb = double.tryParse(_hbCtrl.text);
    final fundal = double.tryParse(_fundalCtrl.text);

    if (sys == null || dia == null || hb == null || fundal == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please fill all vitals')),
      );
      return;
    }

    setState(() {
      _loading = true;
      _detectedRisk = _quickRisk();
    });

    try {
      final result = await GemmaService().assessVitals(
        patientName: widget.patient.name,
        weeks: widget.patient.weeksPregnant,
        systolic: sys,
        diastolic: dia,
        hemoglobin: hb,
        fundalHeight: fundal,
        hasOedema: _hasOedema,
        language: widget.language,
      );
      setState(() {
        _assessment = result;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _loading = false;
        _assessment = 'Error: ${e.toString()}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFF8F0),
      appBar: AppBar(
        backgroundColor: const Color(0xFF8B1A1A),
        foregroundColor: Colors.white,
        title: Text(
          widget.patient.name,
          style: GoogleFonts.poppins(fontWeight: FontWeight.w600),
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 12),
            child: Center(child: RiskBadge(level: widget.patient.riskLevel)),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _infoRow('Village', widget.patient.village),
            _infoRow('Weeks', '${widget.patient.weeksPregnant} weeks'),
            const SizedBox(height: 20),
            Text(
              'Today\'s Vitals',
              style: GoogleFonts.poppins(
                fontWeight: FontWeight.w600,
                fontSize: 16,
              ),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _VitalField(
                    label: 'Systolic BP',
                    hint: '120',
                    unit: 'mmHg',
                    controller: _systolicCtrl,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _VitalField(
                    label: 'Diastolic BP',
                    hint: '80',
                    unit: 'mmHg',
                    controller: _diastolicCtrl,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _VitalField(
                    label: 'Haemoglobin',
                    hint: '11.5',
                    unit: 'g/dL',
                    controller: _hbCtrl,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _VitalField(
                    label: 'Fundal Height',
                    hint: '32',
                    unit: 'cm',
                    controller: _fundalCtrl,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            SwitchListTile(
              title: Text(
                'Oedema present',
                style: GoogleFonts.poppins(fontSize: 14),
              ),
              value: _hasOedema,
              onChanged: (v) => setState(() => _hasOedema = v),
              activeThumbColor: const Color(0xFF8B1A1A),
              contentPadding: EdgeInsets.zero,
            ),
            const SizedBox(height: 20),
            if (_detectedRisk != null && !_loading)
              _QuickRiskBanner(level: _detectedRisk!),
            if (_loading)
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(20),
                  child: CircularProgressIndicator(color: Color(0xFF8B1A1A)),
                ),
              ),
            if (_assessment != null && !_loading) ...[
              const SizedBox(height: 16),
              _AssessmentCard(text: _assessment!),
            ],
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF8B1A1A),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                onPressed: _loading ? null : _assess,
                icon: const Icon(Icons.psychology_outlined),
                label: Text(
                  'Gemma ගෙන් අසන්න · Get AI Assessment',
                  style: GoogleFonts.poppins(fontWeight: FontWeight.w600),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _infoRow(String label, String value) => Padding(
        padding: const EdgeInsets.only(bottom: 4),
        child: Row(
          children: [
            Text('$label: ',
                style: GoogleFonts.poppins(
                    fontSize: 13, color: Colors.grey[500])),
            Text(value,
                style: GoogleFonts.poppins(
                    fontSize: 13, fontWeight: FontWeight.w500)),
          ],
        ),
      );
}

class _VitalField extends StatelessWidget {
  final String label;
  final String hint;
  final String unit;
  final TextEditingController controller;
  const _VitalField(
      {required this.label,
      required this.hint,
      required this.unit,
      required this.controller});

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      keyboardType: const TextInputType.numberWithOptions(decimal: true),
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        suffixText: unit,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      ),
    );
  }
}

class _QuickRiskBanner extends StatelessWidget {
  final RiskLevel level;
  const _QuickRiskBanner({required this.level});

  @override
  Widget build(BuildContext context) {
    final (color, text) = switch (level) {
      RiskLevel.urgent => (
          const Color(0xFFD32F2F),
          'URGENT — Refer to hospital immediately'
        ),
      RiskLevel.high => (
          const Color(0xFFE65100),
          'HIGH RISK — Close monitoring required'
        ),
      RiskLevel.medium => (
          const Color(0xFFF9A825),
          'MEDIUM — Follow up within 2 weeks'
        ),
      RiskLevel.low => (
          const Color(0xFF2E7D32),
          'LOW RISK — Routine follow-up'
        ),
    };
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        border: Border.all(color: color),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Text(
        text,
        style: GoogleFonts.poppins(
          fontWeight: FontWeight.w600,
          color: color,
          fontSize: 14,
        ),
      ),
    );
  }
}

class _AssessmentCard extends StatelessWidget {
  final String text;
  const _AssessmentCard({required this.text});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
              color: Colors.black.withValues(alpha: 0.07),
              blurRadius: 8,
              offset: const Offset(0, 2)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.psychology_outlined,
                  color: Color(0xFF8B1A1A), size: 18),
              const SizedBox(width: 6),
              Text(
                'Gemma Assessment',
                style: GoogleFonts.poppins(
                  fontWeight: FontWeight.w600,
                  fontSize: 13,
                  color: const Color(0xFF8B1A1A),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(text, style: GoogleFonts.notoSansSinhala(fontSize: 14, height: 1.5)),
        ],
      ),
    );
  }
}
