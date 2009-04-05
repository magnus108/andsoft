import javax.swing.*;
import java.awt.*;

class Case extends JTextField
{
    private CaseInfo ci = new CaseInfo();
    private boolean fixed = false;

    Case()
    {
	super("123456789");
	setEditable(false);
    }

    void forbidValue(int value, Color color)
    {
	int wasFixed = ci.isFixed();
	if (!fixed) 
	{
	    ci.forbidValue(value);
	    setText(ci.toString());
	}
	    
	if (wasFixed == -1)
	{
	    int isFixed = ci.isFixed();
	    if (isFixed != -1)
		setBackground(color);
	}
    }

    void setFixed(int value)
    {
	ci.setFixed(value);
	setText(ci.toString());
	fixed = true;
	setBackground(Color.GREEN);
    }

    void newFixed(int value)
    {
	int isFixed = ci.isFixed();
	if (isFixed == -1)
	{
	    ci.setFixed(value);
	    setText(ci.toString());
	    fixed = true;
	    setBackground(Color.RED);
	}
    }

    boolean allowValue(int value)
    {
	return ci.allowValue(value);
    }

    int isFixed()
    {
	return ci.isFixed();
    }
}