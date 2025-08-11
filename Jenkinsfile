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
          bash -lc '
            set -Eeuo pipefail
            python3 -m venv .venv
            source .venv/bin/activate
            python --version
            pip install --upgrade pip
            pip install -r requirements.txt
            python scripts/btc_to_csv.py
            echo "Workspace:"
            ls -la
          '
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
