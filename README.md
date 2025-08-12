# PDF Text Extraction Benchmark

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/GitHub_Codespaces-181717?logo=github&logoColor=white" alt="GitHub Codespaces">
</div>

A comprehensive benchmark tool for comparing PDF text extraction tools (MinerU, Marker, Cog Marker) with a modern web interface.

## 🌍 Languages / Sprachen

- [English](#-features) (below)
- [Deutsch](#-funktionen)

---

## 🚀 Features

- **Web-based Interface**: Modern, responsive UI built with Streamlit
- **Multi-language Support**: English and German interface
- **Comprehensive Comparison**: Detailed metrics for each extraction tool
- **Visual Analytics**: Interactive charts and performance metrics
- **Docker & Codespaces Ready**: Run locally or in the cloud

## 🛠 Setup

### Prerequisites

- Docker and Docker Compose (for local development)
- Python 3.10+ (if not using Docker)
- Git

### Quick Start with GitHub Codespaces

1. Click on the "Code" button and select "Open with Codespaces"
2. Create a new codespace on main branch
3. Once the container is built, the app will automatically start
4. Access the app at the URL shown in the terminal

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdf-benchmark.git
   cd pdf-benchmark
   ```

2. Start with Docker Compose (recommended):
   ```bash
   docker-compose up --build
   ```
   Then open http://localhost:8501 in your browser

3. Or run directly with Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

## 📊 Usage

1. Select the folder containing your PDF files
2. Click "Run Benchmark" to start the comparison
3. View detailed results including:
   - Extraction success rates
   - Processing times
   - Text quality metrics
   - Visual comparisons

## 📂 Project Structure

```
.
├── .devcontainer/          # VS Code dev container configuration
├── .github/workflows/      # CI/CD pipelines
├── data/                   # Default directory for PDFs and results
├── app.py                  # Main Streamlit application
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
└── requirements.txt        # Python dependencies
```

## 📈 Performance Metrics

The benchmark measures:

- **Extraction Time**: How long each tool takes to process a PDF
- **Success Rate**: Percentage of successfully processed files
- **Text Quality**: Character count and extraction accuracy
- **Resource Usage**: CPU and memory consumption

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🚀 Funktionen

- **Web-basierte Benutzeroberfläche**: Moderne, responsive Oberfläche mit Streamlit
- **Mehrsprachige Unterstützung**: Deutsch und Englisch
- **Umfassender Vergleich**: Detaillierte Metriken für jedes Extraktionstool
- **Visuelle Analysen**: Interaktive Diagramme und Leistungsmetriken
- **Docker & Codespaces bereit**: Lokal oder in der Cloud ausführen

## 🛠 Einrichtung

### Voraussetzungen

- Docker und Docker Compose (für die lokale Entwicklung)
- Python 3.10+ (wenn Docker nicht verwendet wird)
- Git

### Schnellstart mit GitHub Codespaces

1. Klicken Sie auf den "Code"-Button und wählen Sie "Mit Codespaces öffnen"
2. Erstellen Sie einen neuen Codespace auf dem main-Branch
3. Sobald der Container erstellt wurde, startet die App automatisch
4. Greifen Sie über die im Terminal angezeigte URL auf die App zu

### Lokale Entwicklung

1. Repository klonen:
   ```bash
   git clone https://github.com/ihrbenutzername/pdf-benchmark.git
   cd pdf-benchmark
   ```

2. Mit Docker Compose starten (empfohlen):
   ```bash
   docker-compose up --build
   ```
   Dann öffnen Sie http://localhost:8501 in Ihrem Browser

3. Oder direkt mit Python ausführen:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

## 📊 Verwendung

1. Wählen Sie den Ordner mit Ihren PDF-Dateien aus
2. Klicken Sie auf "Benchmark starten", um den Vergleich zu beginnen
3. Sehen Sie sich detaillierte Ergebnisse an, darunter:
   - Erfolgsraten der Extraktion
   - Verarbeitungszeiten
   - Textqualitätsmetriken
   - Visuelle Vergleiche

## 📈 Leistungsmetriken

Der Benchmark misst:

- **Extraktionszeit**: Wie lange jedes Tool für die Verarbeitung einer PDF benötigt
- **Erfolgsrate**: Prozentsatz der erfolgreich verarbeiteten Dateien
- **Textqualität**: Zeichenanzahl und Extraktionsgenauigkeit
- **Ressourcennutzung**: CPU- und Speicherverbrauch
