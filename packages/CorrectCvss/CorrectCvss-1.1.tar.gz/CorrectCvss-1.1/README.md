# CorrectCvss 

## Function Introduction



Correct the order of CVSS2 vectors and check for validity.

case:

```
from CorrectCvss.correct_cvss import correct_cvss2_vector

correct_cvss2_vector(cvss2_vector)
```



Correct the order of CVSS3 vectors and check for validity.

case:

```
from CorrectCvss.correct_cvss import correct_cvss3_vector

correct_cvss3_vector(cvss3_vector, 3.0)
correct_cvss3_vector(cvss3_vector, 3.1)
```



Corrected the order of CVSS4.0 vectors and checked validity.

case:

```
from CorrectCvss.correct_cvss import correct_cvss4_vector

correct_cvss4_vector(cvss4_vector)
```

