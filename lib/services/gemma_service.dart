import 'dart:io';
import 'package:flutter_gemma/flutter_gemma.dart';
import 'package:path_provider/path_provider.dart';

// Gemma 4 E2B (Edge 2B) in LiteRT format — ~2.6GB
// Apache 2.0 license — no HuggingFace token required
// Qualifies for LiteRT special prize ($10k) + Gemma 4 hackathon eligibility
const _modelUrl =
    'https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm/resolve/main/gemma-4-E2B-it.litertlm';

const _modelFilename = 'gemma-4-E2B-it.litertlm';

const _systemInstruction = '''
You are Amma Sewana, an AI assistant for Sri Lanka Public Health Midwives (PHMs).
Help PHMs assess pregnant mothers and answer clinical questions.
Follow Sri Lanka Ministry of Health maternal care guidelines.

DANGER SIGNS — always start reply with "URGENT":
- Systolic BP >= 160 or diastolic >= 100
- Haemoglobin < 8 g/dL (severe anaemia)
- Absent fetal movement > 12 hours
- Severe oedema (face + hands)
- Severe headache + visual disturbances + high BP

NORMAL RANGES:
- BP: <140/90 normal, 140-159/90-99 watch, >=160/100 URGENT
- Haemoglobin: >11 normal, 9-11 mild, <9 moderate, <8 severe
- Fundal height: gestational weeks +/- 3 cm acceptable

Keep answers short and action-oriented. Always say when to refer to hospital.
Reply in the same language as the question (Sinhala, Tamil, or English).''';

class GemmaService {
  static final GemmaService _instance = GemmaService._internal();
  factory GemmaService() => _instance;
  GemmaService._internal();

  InferenceModel? _model;
  InferenceChat? _chat;

  bool get hasActiveModel => FlutterGemma.hasActiveModel();

  Future<void> downloadModel({
    required void Function(int progress) onProgress,
  }) async {
    final extDir = await getExternalStorageDirectory();
    final localFile = File('${extDir!.path}/$_modelFilename');
    final builder = FlutterGemma.installModel(
      modelType: ModelType.gemma4,
      fileType: ModelFileType.litertlm,
    );
    if (await localFile.exists()) {
      await builder.fromFile(localFile.path).withProgress(onProgress).install();
    } else {
      await builder.fromNetwork(_modelUrl).withProgress(onProgress).install();
    }
  }

  Future<void> initialize() async {
    if (_model != null) return;
    _model = await FlutterGemma.getActiveModel(
      maxTokens: 2048,
      preferredBackend: PreferredBackend.gpu,
    );
  }

  Future<void> resetChat() async {
    _chat?.close();
    _chat = null;
    if (_model == null) await initialize();
    _chat = await _model!.createChat(
      temperature: 0.3,
      topK: 40,
      modelType: ModelType.gemma4,
      systemInstruction: _systemInstruction,
    );
  }

  Stream<String> chat(String userMessage) async* {
    if (_model == null) await initialize();
    _chat ??= await _model!.createChat(
      temperature: 0.3,
      topK: 40,
      modelType: ModelType.gemma4,
      systemInstruction: _systemInstruction,
    );
    await _chat!.addQueryChunk(Message(text: userMessage, isUser: true));
    await for (final response in _chat!.generateChatResponseAsync()) {
      if (response is TextResponse) yield response.token;
    }
  }

  Future<String> assessVitals({
    required String patientName,
    required int weeks,
    required int systolic,
    required int diastolic,
    required double hemoglobin,
    required double fundalHeight,
    required bool hasOedema,
    required String language,
  }) async {
    final langInstruction = switch (language) {
      'sinhala' => 'Reply in Sinhala only.',
      'tamil' => 'Reply in Tamil only.',
      _ => 'Reply in English only.',
    };

    final prompt =
        '$langInstruction\n\nPatient: $patientName, $weeks weeks pregnant.\n'
        'Vitals: BP $systolic/$diastolic mmHg, Hb ${hemoglobin}g/dL, '
        'Fundal ${fundalHeight}cm, Oedema: ${hasOedema ? "yes" : "no"}.\n\n'
        'State risk level (LOW/MEDIUM/HIGH/URGENT) and one clear action for the PHM.';

    if (_model == null) await initialize();
    final session = await _model!.createSession(
      temperature: 0.2,
      systemInstruction: _systemInstruction,
    );
    await session.addQueryChunk(Message(text: prompt, isUser: true));
    final result = await session.getResponse();
    await session.close();
    return result;
  }
}
