# CPOS Agent Sandbox Company (Local MVP)

Microsoft Agent Hackathon 2026に向けた、AIエージェントによる企業活動シミュレーション環境のMVPです。

## 概要
Planner, Dev, Security, Reviewの4つのエージェントが、企画から開発、セキュリティ監査、レビューまでのサイクルを自律的に回します。すべての活動ログと文脈（Pointers）はCPOS（Context Pointer OS）の仕様に基づいて保存されます。

## 機能
- **PlannerAgent**: プロダクトの仕様（Spec）を策定。
- **DevAgent**: 仕様に基づきPythonコードを生成（意図的な脆弱性と不備を含む）。
- **SecurityAgent**: 生成されたコードをルールベースでスキャン。
- **SandboxRunner**: `ruff` によるLintチェックとコンパイル確認を実行。
- **ReviewAgent**: セキュリティ結果とSandbox結果を統合し、採用・却下を判定。

## 実行手順

1. 依存関係の確認:
   `ruff` がインストールされていることを確認してください。
   ```bash
   pip install ruff
   ```

2. MVPの実行:
   ```bash
   cd cpos_sandbox_company
   python3 main_controller.py
   ```

3. ログの確認:
   - `cpos/audit_log.jsonl`: エージェントの行動履歴。
   - `cpos/pointers.jsonl`: 生成物やバグへの参照（Context Pointers）。
   - `outputs/python_tools/`: 生成された成果物。

## Hackathon Roadmap
- Phase 2: Web Dashboardの実装（リアルタイムモニタリング）。
- Phase 3: Azure (OpenAI / Container Apps) への統合。
- Phase 4: GitHub連携と成果物の自動永続化。
