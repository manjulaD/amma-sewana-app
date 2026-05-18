import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/patient.dart';
import '../services/gemma_service.dart';

const _suggestions = {
  'sinhala': [
    'රුධිර පීඩනය 150/95 — කළ යුත්තේ කුමක්ද?',
    'Hb 9.5, 28 සති — යකඩ ගැනීම ප්‍රමාණවත්ද?',
    'කකුල් ඉදිමුම සහ BP නාමාල් — Preeclampsia ලකුණු?',
    'රෝහලට යවන්නේ කවදාද?',
  ],
  'tamil': [
    'BP 150/95 — என்ன செய்ய வேண்டும்?',
    'Hb 9.5, 28 வாரங்கள் — இரும்பு சரியானதா?',
    'கால் வீக்கம் உள்ளது — மருத்துவமனைக்கு அனுப்ப வேண்டுமா?',
  ],
  'english': [
    'BP 150/95 at 32 weeks — what action to take?',
    'Hb 9.5 at 28 weeks — is iron supplement enough?',
    'Leg oedema, normal BP — signs of preeclampsia?',
    'When to refer immediately to hospital?',
  ],
};

class ChatScreen extends StatefulWidget {
  final String language;
  const ChatScreen({super.key, required this.language});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _ctrl = TextEditingController();
  final _scrollCtrl = ScrollController();
  final List<ChatMessage> _messages = [];
  bool _thinking = false;
  String _streamBuffer = '';

  @override
  void initState() {
    super.initState();
    GemmaService().resetChat();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    _scrollCtrl.dispose();
    super.dispose();
  }

  Future<void> _send(String text) async {
    if (text.trim().isEmpty) return;
    _ctrl.clear();
    setState(() {
      _messages.add(ChatMessage(text: text, isUser: true));
      _thinking = true;
      _streamBuffer = '';
    });
    _scrollToBottom();

    try {
      await for (final token in GemmaService().chat(text)) {
        setState(() => _streamBuffer += token);
        _scrollToBottom();
      }
      setState(() {
        _messages.add(ChatMessage(text: _streamBuffer, isUser: false));
        _streamBuffer = '';
        _thinking = false;
      });
    } catch (e) {
      setState(() {
        _messages.add(
          ChatMessage(text: 'Error: ${e.toString()}', isUser: false),
        );
        _thinking = false;
      });
    }
    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollCtrl.hasClients) {
        _scrollCtrl.animateTo(
          _scrollCtrl.position.maxScrollExtent,
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final suggestions = _suggestions[widget.language] ?? _suggestions['english']!;

    return Scaffold(
      backgroundColor: const Color(0xFFFFF8F0),
      appBar: AppBar(
        backgroundColor: const Color(0xFF8B1A1A),
        foregroundColor: Colors.white,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Gemma · On-device AI',
                style: GoogleFonts.poppins(
                    fontWeight: FontWeight.w600, fontSize: 15)),
            Text('Gemma 3 1B · offline',
                style: GoogleFonts.poppins(fontSize: 10)),
          ],
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: _messages.isEmpty
                ? _buildSuggestions(suggestions)
                : _buildMessageList(),
          ),
          if (_thinking && _streamBuffer.isNotEmpty)
            _StreamingBubble(text: _streamBuffer),
          _InputBar(
            controller: _ctrl,
            onSend: _send,
            thinking: _thinking,
          ),
        ],
      ),
    );
  }

  Widget _buildSuggestions(List<String> suggestions) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const SizedBox(height: 12),
        Center(
          child: Column(
            children: [
              const Icon(Icons.psychology_outlined,
                  size: 48, color: Color(0xFF8B1A1A)),
              const SizedBox(height: 8),
              Text(
                'Ask anything about maternal health',
                style: GoogleFonts.poppins(
                    color: Colors.grey[600], fontSize: 13),
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        ...suggestions.map(
          (s) => GestureDetector(
            onTap: () => _send(s),
            child: Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding:
                  const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: Colors.white,
                border: Border.all(color: const Color(0xFF8B1A1A).withValues(alpha: 0.3)),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Text(
                s,
                style: GoogleFonts.notoSansSinhala(
                    fontSize: 13, color: Colors.grey[800]),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildMessageList() {
    return ListView.builder(
      controller: _scrollCtrl,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      itemCount: _messages.length,
      itemBuilder: (_, i) => _MessageBubble(message: _messages[i]),
    );
  }
}

class _MessageBubble extends StatelessWidget {
  final ChatMessage message;
  const _MessageBubble({required this.message});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment:
          message.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 8),
        padding:
            const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width * 0.8),
        decoration: BoxDecoration(
          color: message.isUser
              ? const Color(0xFF8B1A1A)
              : Colors.white,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(12),
            topRight: const Radius.circular(12),
            bottomLeft: Radius.circular(message.isUser ? 12 : 0),
            bottomRight: Radius.circular(message.isUser ? 0 : 12),
          ),
          boxShadow: [
            BoxShadow(
                color: Colors.black.withValues(alpha: 0.06),
                blurRadius: 4,
                offset: const Offset(0, 1)),
          ],
        ),
        child: Text(
          message.text,
          style: GoogleFonts.notoSansSinhala(
            fontSize: 14,
            color: message.isUser ? Colors.white : Colors.grey[800],
            height: 1.5,
          ),
        ),
      ),
    );
  }
}

class _StreamingBubble extends StatelessWidget {
  final String text;
  const _StreamingBubble({required this.text});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.fromLTRB(12, 0, 60, 4),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: const BorderRadius.only(
            topLeft: Radius.circular(12),
            topRight: Radius.circular(12),
            bottomRight: Radius.circular(12),
          ),
        ),
        child: Text(
          text,
          style: GoogleFonts.notoSansSinhala(fontSize: 14, height: 1.5),
        ),
      ),
    );
  }
}

class _InputBar extends StatelessWidget {
  final TextEditingController controller;
  final void Function(String) onSend;
  final bool thinking;
  const _InputBar(
      {required this.controller,
      required this.onSend,
      required this.thinking});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(12, 8, 8, 16),
      color: Colors.white,
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: controller,
              enabled: !thinking,
              maxLines: null,
              textInputAction: TextInputAction.send,
              onSubmitted: onSend,
              decoration: InputDecoration(
                hintText: 'Ask in Sinhala, Tamil, or English...',
                hintStyle:
                    GoogleFonts.poppins(fontSize: 13, color: Colors.grey[400]),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(24),
                  borderSide: BorderSide.none,
                ),
                filled: true,
                fillColor: const Color(0xFFF5F5F5),
                contentPadding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              ),
            ),
          ),
          const SizedBox(width: 8),
          AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            child: IconButton(
              onPressed: thinking ? null : () => onSend(controller.text),
              icon: thinking
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                          strokeWidth: 2, color: Color(0xFF8B1A1A)),
                    )
                  : const Icon(Icons.send_rounded, color: Color(0xFF8B1A1A)),
            ),
          ),
        ],
      ),
    );
  }
}
