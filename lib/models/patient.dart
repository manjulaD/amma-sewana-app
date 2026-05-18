enum RiskLevel { low, medium, high, urgent }

class Patient {
  final String id;
  final String name;
  final String nameSinhala;
  final String village;
  final int weeksPregnant;
  final RiskLevel riskLevel;
  final DateTime lastVisit;

  const Patient({
    required this.id,
    required this.name,
    required this.nameSinhala,
    required this.village,
    required this.weeksPregnant,
    required this.riskLevel,
    required this.lastVisit,
  });
}

class VitalSigns {
  final int systolic;
  final int diastolic;
  final double hemoglobin;
  final double fundalHeight;
  final bool hasOedema;
  final bool hasDizziness;
  final String fetalMovement; // 'normal', 'reduced', 'absent'

  const VitalSigns({
    required this.systolic,
    required this.diastolic,
    required this.hemoglobin,
    required this.fundalHeight,
    required this.hasOedema,
    this.hasDizziness = false,
    this.fetalMovement = 'normal',
  });
}

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;

  ChatMessage({
    required this.text,
    required this.isUser,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();
}
