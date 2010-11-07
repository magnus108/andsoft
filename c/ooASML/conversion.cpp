/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#include <asml/utils/error.h>
#include "conversion.h"

using namespace ::com::sun::star::uno;
using namespace ::rtl;

namespace ASI
{
    template<>
    void ooConvert(const OUString & s1, std::string & str)
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

    template <>
    void ooConvert(const std::string & str, OUString & s1)
    {
        s1 = OUString::createFromAscii(str.c_str());
    }

    template <>
    void ooConvert(const Sequence<Sequence<double> >& mat, MatrixPtr & matPtr)
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
    
    template <>
    void ooConvert(const MatrixPtr & matPtr, Sequence<Sequence<double> > & mat)
    {
        const size_t rows = matPtr->size1;
        const size_t cols = matPtr->size2;
        
        mat = Sequence<Sequence<double> >(rows);
        
        for (size_t i = 0; i < rows; ++i)
        {
            mat[i].realloc(cols);
            for (size_t j = 0; j < cols; ++j)
            {
                mat[i][j] = gsl_matrix_get(matPtr.get(), i, j);
            }
        }
    }
    
    template <>
    void ooConvert(const Sequence<Sequence<double> >& vect, VectorPtr & vectPtr)
    {
        MatrixPtr matrix;
        ooConvert(vect, matrix);
        
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
    
    template <>
    void ooConvert(const VectorPtr & vectPtr, Sequence<Sequence<double> >& vect)
    {
        const size_t rows = vectPtr->size;
        const size_t cols = 1;
        
        vect = Sequence<Sequence<double> > (rows);
        
        for (size_t i = 0; i < rows; ++i)
        {
            vect[i].realloc(cols);
            vect[i][0] = gsl_vector_get(vectPtr.get(), i);
        }
    }
    
    template <>
    void ooConvert(const Sequence<Sequence<double> >& vect, std::vector<double> & stdVect)
    {
        VectorPtr vector;
        ooConvert(vect, vector);
        
        const size_t dim = vector->size;
        
        stdVect.resize(dim);
        
        for (size_t i = 0; i < dim; ++i)
        {
            stdVect[i] = gsl_vector_get(vector.get(), i);
        }
    }
    
    template <>
    void ooConvert(const std::vector<double> & stdVect, Sequence<Sequence<double> >& vect)
    {
        const size_t rows = stdVect.size();
        const size_t cols = 1;
        
        vect = Sequence<Sequence<double> > (rows);
        
        for (size_t i = 0; i < rows; ++i)
        {
            vect[i].realloc(cols);
            vect[i][0] = stdVect[i];
        }
    }
    
    void appendStdVectorToOOArgument(Sequence<Sequence<double> > & seq, const std::vector<double> & vect)
    {
        const size_t rows = seq.getLength();
        const size_t vect_rows = vect.size();
        
        if (rows == 0)
            seq.realloc(vect_rows);
        else
            if (vect.size() != rows)
                error("size mismatch!");
        
        for (size_t i = 0; i < vect_rows; ++i)
        {
            const size_t cols = seq[i].getLength();
            seq[i].realloc(cols + 1);
            seq[i][cols] = vect[i];
        }
    }
    
    template <>
    void ooConvert(const Sequence<double> & vect, cpl & cplNum)
    {
        std::vector<double> v;
        ooConvert(vect, v);
        
        const size_t cols = v.size();
        
        if (cols != 2)
            error("For complex data, there must be 2 columns");
        
        cplNum = cpl(v[0], v[1]);
    }
    
    template <>
    void ooConvert(const cpl & cplNum, Sequence<double> & vect)
    {
        vect = Sequence<double> (2);
        
        vect[0] = cplNum.real();
        vect[1] = cplNum.imag();
    }
}
