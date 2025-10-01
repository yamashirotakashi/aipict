# Agents 提議メモ

## プロジェクト概要
- プロジェクト名: **aipict**
- 目的: Ryzen™ AI Max+ 395 / Radeon 8060S 環境のWSL上に、AMD GPU(ROCm)対応の生成AI画像制作スタックを構築し、公開モデル・LoRAの運用を本番水準で実行可能にする。
- 背景: Windows側ではSD.Nextが検証用途で稼働済み。本プロジェクトはWSLを主軸に、再現性・可観測性・データガバナンスを強化することを狙う。

## 参画エージェントと責務
- **Serena**: タスク分解、フェーズごとのTODO生成、成功条件と回復手順を備えたDAG管理。
- **Cipher**: セキュリティ・ライセンス・依存バージョン固定のレビュー、およびSBOM整備提案。
- **Zen**: トラブル発生時の原因切り分け、最小再現パスの提示、復旧フローチャート化。
- **Codex CLI**: 上記エージェントをドライバーとして呼び出し、WSL環境での自動化コマンドを実行する統制役。

## 開発原則
1. 仕様書駆動開発 (Specification → Design → Implementation → Test)
2. テスト駆動開発 (Red-Green-Refactor) を全スクリプト・テンプレで遵守
3. 単一責任原則 (SRP) に基づくモジュール分割とドキュメント連携

## 成果物
- `docs/xml/specification.xml` : 機能要件・非機能要件
- `docs/xml/design.xml` : レイヤードアーキテクチャ設計
- `docs/xml/roadmap.xml` : 5フェーズロードマップ
- 将来的に追加予定の自動化スクリプト、テストスイート、エージェント連携テンプレート

## 合意事項
- リポジトリ: GitHub `yamashirotakashi/aipict`
- 認証情報: `.env` 管理。公開コミットには含めない。
- ドキュメント言語: 日本語（必要に応じて英語版を追加）
- テスト: 仕様書のTraceabilityに基づき、CI環境（GitHub Actions想定）で自動化

## 次のアクション
1. docs/xml配下の仕様・設計・ロードマップに沿うテストケース一覧の草案化
2. agentsごとの実行テンプレート（Codex CLI用）雛形を追加
3. Stage 1 のWSL+ROCmセットアップ手順をスクリプト化し、TDDで検証
