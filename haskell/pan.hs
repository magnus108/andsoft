import Elves.Pan
import Data.Map
import Data.Set
import Data.List

one = 1 :: FloatE
var = "x"
x = varFloatE var
y = varFloatE "y"
ctx = Data.Map.fromList [(var, 4 :: Float)]

f y = (castFloatE y) * (x + one)
arr = mkArray 5 f
pos = ifE (x >* 5) (1 :: IntE) 2
ele = (readArr arr (castIntE x)) * (x + one)

chk = ifE (x >* 5) one (one + one)

showLinear f = concat (intersperse "\n" (Prelude.map show f))

cpl = ifE (x >* y) (x + x + y) ((x + x) * (x + x))
