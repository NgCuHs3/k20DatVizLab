
echo "run all cell for html chart"

jupyter nbconvert --to notebook --inplace --execute .\Labcode\chartlab.ipynb

echo "clear out put"
jupyter nbconvert --clear-output --inplace .\Labcode\chartlab.ipynb

python ./Labcode/generateDOM.py

.\sitedeploy.cmd