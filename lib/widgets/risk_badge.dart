import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/patient.dart';

class RiskBadge extends StatelessWidget {
  final RiskLevel level;
  const RiskBadge({super.key, required this.level});

  @override
  Widget build(BuildContext context) {
    final (color, label) = switch (level) {
      RiskLevel.urgent => (const Color(0xFFD32F2F), 'URGENT'),
      RiskLevel.high => (const Color(0xFFE65100), 'HIGH'),
      RiskLevel.medium => (const Color(0xFFF9A825), 'MEDIUM'),
      RiskLevel.low => (const Color(0xFF2E7D32), 'LOW'),
    };
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        border: Border.all(color: color, width: 1.2),
        borderRadius: BorderRadius.circular(6),
      ),
      child: Text(
        label,
        style: GoogleFonts.poppins(
          fontSize: 11,
          fontWeight: FontWeight.w700,
          color: color,
        ),
      ),
    );
  }
}
