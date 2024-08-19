
# hatchをつかって管理する

好みの方法でhatchをインストールする
※ OS上に直接インストールできるが、私はpython環境以外を汚したくないのでpipを使った。
```
pip install hatch
```

# テスト

以下を実行し
```
hatch shell tests 
```
テスト用仮想環境に入り
```
hatch test
```
でパッケージに対するテストが実行できます


