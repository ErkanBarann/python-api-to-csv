pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup & Run') {
      steps {
        sh '''
          set -eux   # pipefail yoksa sorun çıkmasın
          python3 -m venv .venv
          . .venv/bin/activate
          python --version
          pip install --upgrade pip
          pip install -r requirements.txt
          python scripts/btc_to_csv.py
          echo "Workspace listesi:"
          ls -la
        '''
      }
    }

    stage('Archive CSV') {
      steps {
        archiveArtifacts artifacts: 'btc_price.csv', onlyIfSuccessful: true, fingerprint: true
      }
    }
  }
}
