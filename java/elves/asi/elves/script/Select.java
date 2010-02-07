package asi.elves.script;

import java.util.*;
import asi.elves.*;

/**
 *
 * Select a subset of a TimeSeries
 */
public class Select implements TimeSeries
{
    private TimeSeries m_Value;
    private int m_First;
    private int m_Last;
    
    /**
     * Select a subset of a TimeSeries
     * <p>
     * Use negative indices to index frm the end of the list
     *
     * @param value Original time series
     * @param first initial point (inclusive)
     * @param last final point (exclusive)
     */
    public Select(TimeSeries value, int first, int last)
    {
        m_Value = value;
        int size = m_Value.dates().size();
        m_First = first < 0 ? first + size : first;
        m_Last  = last  < 0 ? last  + size : last;
    }

    public List<Date> dates()
    {
        return m_Value.dates().subList(m_First, m_Last);
    }

    public void values(Path path, Memoizer storage)
    {
        List<Double> values = storage.get(m_Value);
        storage.put(this, values.subList(m_First, m_Last));
    }

    public List<TimeSeries> children()
    {
        return Arrays.asList(m_Value);
    }


}
