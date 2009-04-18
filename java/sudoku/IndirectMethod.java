import java.awt.*;

class IndirectMethod extends SuDokuMethod
{

    IndirectMethod(Case[][] guesses, Case[][] rows, Case[][] cols, Case[][] blocks)
    {
        super(guesses, rows, cols, blocks);
    }

	private void lookForDoublesInOneSquare(int r, int c)
	{
		for (int number = 0; number < 9; ++number)
		{
			int count = 0;
			int first_r = -1;
			int first_c = -1;
			int row_base = r * 3;
			int col_base = c * 3;
			for (int row = row_base; row < row_base + 3; ++row)
			{
				for (int col = col_base; col < col_base + 3; ++col)
				{
					if (guesses[row][col].isValid(number))
					{
						++count;
						if (count == 1)
						{
							first_r = row;
							first_c = col;
						}
						else
						{
							if (first_r == row)
							{
								first_c = -1;
							}
							else
							{
								if (first_c == col)
								{
									first_r = -1;
								}
								else
								{
									first_r = -1;
									first_c = -1;
								}
							}
						}
					}
				}
			}
			if (first_r != -1)
			{
				for (int col = 0; col < 9; ++col)
				{
					int c2 = col / 3;
					if (c2 != c)
						guesses[first_r][col].forbidValue(number, Color.WHITE);
				}
			}
			if (first_c != -1)
			{
				for (int row = 0; row < 9; ++row)
				{
					int r2 = row / 3;
					if (r2 != r)
						guesses[row][first_c].forbidValue(number, Color.WHITE);
				}
			}
		}
	}

	private void secondPass()
	{
		for (int r = 0; r < 3; ++r)
			for (int c = 0; c < 3; ++c)
				lookForDoublesInOneSquare(r, c);
	}

    void solve()
    {
        secondPass();
    }

}
