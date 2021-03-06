/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#include <asml/utils/error.h>
#include "ConversionIn.h"
#include <boost/regex.hpp> 
#include <boost/lexical_cast.hpp> 

using namespace ::com::sun::star::uno;
using namespace ::rtl;

namespace ASI
{
    void ooConvertIn(const OUString & s1, std::string & str)
    {
        OString s2;
        if (s1.convertToString(&s2, RTL_TEXTENCODING_ASCII_US, OUSTRING_TO_OSTRING_CVTFLAGS))
        {
            str = std::string(s2.getStr());
        }
        else
        {
            THROW_EXCEPTION("Unable to convert string");
        }
    }

    void ooConvertIn(double val, QuantLib::Date & date)
    {
        date = QuantLib::Date(val);
    }

    void ooConvertIn(const Sequence<Sequence<double> >& mat, MatrixPtr & matPtr)
    {
        const size_t rows = mat.getLength();
        
        size_t cols = 0;
        
        for (size_t i = 0; i < rows; ++i)
        {
            cols = std::max(cols, size_t(mat[i].getLength()));
        }
        
        matPtr.reset(gsl_matrix_calloc(rows, cols), MatrixDeleter());
        
        for (size_t i = 0; i < rows; ++i)
        {
            size_t thisCols = mat[i].getLength();
            for (size_t j = 0; j < thisCols; ++j)
            {
                gsl_matrix_set (matPtr.get(), i, j, mat[i][j]);
            }
            
        }
    }
    
    void ooConvertIn(const Sequence<Sequence<double> >& vect, VectorPtr & vectPtr)
    {
        MatrixPtr matrix;
        ooConvertIn(vect, matrix);
        
        if (matrix->size1 == 1)
        {
            // row vector
            const size_t len = matrix->size2;
            vectPtr.reset(gsl_vector_calloc(len), VectorDeleter());
            gsl_matrix_get_row (vectPtr.get(), matrix.get(), 0);
            return;
        }
        else if (matrix->size2 == 1)
        {
            // column vector
            const size_t len = matrix->size1;
            vectPtr.reset(gsl_vector_calloc(len), VectorDeleter());
            gsl_matrix_get_col (vectPtr.get(), matrix.get(), 0);
            return;
        }
        else
        {
            error("Not a vector");
        }
    }
    
    void ooConvertIn(const OUString & cplStr, cpl & cplNum)
    {
        std::string s;
        ooConvertIn(cplStr, s);
        
        boost::regex expression("([+-]?[0-9]*)([+-][0-9]*)[iI]");
        boost::smatch what;
        if (!boost::regex_match(s, what, expression))
            THROW_EXCEPTION(s << " is not a valid complex number");

        if (what.size() != 3 || !what[1].matched || !what[2].matched)
            THROW_EXCEPTION("Something went wrong while matching: " << s);

        const std::string realStr = what[1];
        const std::string imgStr  = what[2];

        const double real = boost::lexical_cast<double>(realStr);
        const double img  = boost::lexical_cast<double>(imgStr);

        cplNum = cpl(real, img);
    }

    void ooConvertIn(const Sequence< Sequence< Any> > & a, LVB_t & lvb)
    {
        lvb.clear();
        const size_t rows = a.getLength();
        if (rows == 0)
            return;

        const size_t cols = a[0].getLength();
        if (cols != 2)
            THROW_EXCEPTION("LVB must contain 2 columns. Found " << cols);

        for (size_t i = 0; i < rows; ++i)
        {
            const Any & label = a[i][0];
            OUString ooLabel;
            if (!(label >>= ooLabel))
            {
                THROW_EXCEPTION("Cannot convert label to string");
            }

            std::string labelStr;
            ooConvertIn(ooLabel, labelStr);

            ASIVariant var;
            ooConvertIn(a[i][1], lvb[labelStr]);
        }
    }

    void ooConvertIn(const Any & a, ASIVariant & var)
    {
        const OUString ooTypeName = a.getValueTypeName();

        std::string typeName;
        ooConvertIn(ooTypeName, typeName);

        if (typeName == "string")
        {
            OUString ooS;
            if (!(a >>= ooS))
                THROW_EXCEPTION("any of type string cannot be converted to OUString.");

            std::string str;
            ooConvertIn(ooS, str);

            var = str;
        }
        else if (typeName == "double")
        {
            double val;
            if (!(a >>= val))
                THROW_EXCEPTION("any of type double cannot be converted.");

            var = val;
        }
        else
        {
            THROW_EXCEPTION("Unknown Any type: " << typeName);
        }

    }

    
}
