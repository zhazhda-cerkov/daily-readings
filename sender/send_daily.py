name: Manual send daily

on:
  workflow_dispatch:

jobs:
  send:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install requests

      - name: Run send_daily.py
        env:
          GREEN_API_ID_INSTANCE: ${{ secrets.GREEN_API_ID_INSTANCE }}
          GREEN_API_TOKEN_INSTANCE: ${{ secrets.GREEN_API_TOKEN_INSTANCE }}
          GREEN_API_CHAT_ID: ${{ secrets.GREEN_API_CHAT_ID }}
        run: python sender/send_daily.py
