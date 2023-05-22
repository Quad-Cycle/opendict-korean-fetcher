# opendict-korean-fetcher ![Generic badge](https://img.shields.io/badge/version-0.1.0-blue.svg)

## Setup

### a. Installation

```bash
python3 -m pip install --user -e .
```

### b. (optional) apikey 추가

우리말샘(opendict-kr) API 이용을 위한 개인 키를 입력합니다. 루트 디렉토리에 apikey.py 파일을 생성합니다.

`apikey.py`:

```py
apikey = 'API_KEY'
```

### c. Neo4j 세션 연결

Python에서 Neo4j 세션 연결을 위해 DB 접근 정보들을 입력합니다.

`graphDBGenerator/graphdb_generator.py`:

```bash
uri = 'bolt://localhost:7687'
username = 'neo4j'
password = 'password'
database_name = 'word-hypernyms'
```

### d. resources 추가

루트 디렉토리에 우리말 샘에서 불러온 xml 파일들을 추가합니다. 파일명은 자유형식이지만, resources 폴더 내에 위치한 파일들만 읽을 수 있습니다. 파일은 우리말샘 사이트 로그인 후 `내 정보 관리 > 사전 내려받기`를 통해 다운 가능합니다. ([링크](https://opendict.korean.go.kr/member/memberDownloadList))

### e. 실행

```bash
python main.py
```

## Contributors
<a href="https://github.com/Tri-Cycle/opendict-korean-fetcher/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Tri-Cycle/opendict-korean-fetcher" />
</a>

Made with [contrib.rocks](https://contrib.rocks).
