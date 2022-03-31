import ssv
import pandas as pd
file = ssv.loadf("run1.ssv")
print(type(file))
print(file)
df = pd.DataFrame(file)
print(df.size)
