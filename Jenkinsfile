pipeline {
  agent any
  options { timestamps() }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Setup Python') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }
    stage('Fetch BTC -> CSV') {
      steps {
        sh '''
          . .venv/bin/activate
          python scripts/btc_to_csv.py
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
