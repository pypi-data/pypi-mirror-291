from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .IntegralAlgebra import IntegralAlgebra
 
import sympy as sp
from ordered_set import OrderedSet

from .IntegralMonomial import IM
from .IntegralPolynomial import IntegralPolynomial 
from .utils import (
    expr_has_symbol, 
    expr_has_symbols
)

def find_A_A0_G_F(IA: IntegralAlgebra,
                    P:IntegralPolynomial) -> tuple[IntegralPolynomial]:
    """
    Algorithm 3
    """
    #try to write P as A − (A0 +int Q)
    P_N = P.get_P_N()
    CST = P.get_cst_terms()
    A = IA.polynomials_subtraction(P_N ,CST)
    A0 = IA.product_P_Coeff(CST,-1)
    P_I = P.get_P_I()
    Q = IA.product_P_Coeff(P_I.cut_P("1+"),-1) 

    # check that A != 0
    if A.is_zero(): return None
    # and check that A is in K[X]  
    if any([M.get_nb_int() for M,_ in A.get_content()]): 
        return None
    
    #convert A to simple polynomial ie sp.Expr
    A_sp = sp.Add(*[M.get_content()[0]*coeff for M,coeff in A.get_content()])
     
    r = []
    for M_i, alpha_i in Q.get_content():
        M0 = M_i.cut('0').get_content()[0]
        print("M0",M0)
        print("A_sp",A_sp)
        print("*IA.order",*IA.order)
        q_i, r_i = sp.reduced(M0, [A_sp], *IA.order, order="lex") 
        q_i = q_i[0]#we use only one pol to reduce so we select qi0
        q_i_mons_coeff = list(q_i.as_coefficients_dict(IA.t).items())
        #return [(m0,coeff0), (m1,coeff1),...]
        r_i_mons_coeff = list(r_i.as_coefficients_dict(IA.t).items())
        q_i_pol = IntegralPolynomial(sp.Add(*[IM(mons)*coeff for mons,coeff in q_i_mons_coeff]))
        r_i_pol = IntegralPolynomial(sp.Add(*[IM(mons)*coeff for mons,coeff in r_i_mons_coeff]))
        r += [(alpha_i, q_i_pol, r_i_pol, M_i)]
        
    G, F = IntegralPolynomial(0), IntegralPolynomial(0)

    # this loop is used to create G and F 
    # G = sum (alpha_i q_i M_i[i1+])
    # F = sum (alpha_i r_i M_i[i1+])
    for alpha_i, q_i, r_i, M_i in r: 
        M_i_cut = IntegralPolynomial(M_i.cut("i1+"))
        M_i_cut_alpha = IA.product_P_Coeff(M_i_cut,alpha_i)
        temp_G = IA.polynomials_product(q_i,M_i_cut_alpha) 
        G = IA.polynomials_add(G,temp_G)
        temp_F = IA.polynomials_product(r_i,M_i_cut_alpha) 
        F = IA.polynomials_add(F,temp_F)
    
    if G.is_zero():
        return None
    
    # check that P = A-(A0+\int (AG+F))
    # going from right to left :
    temp = IA.polynomials_product(A,G)
    temp = IA.integrate_polynomial(IA.polynomials_add(temp,F))
    temp = IA.polynomials_add(A0, temp)
    temp = IA.polynomials_subtraction(A,temp) 
    assert sp.simplify(P.get_sympy_repr() - temp.get_sympy_repr()) == 0
    return (A,A0,G,F)




def update_exp(IA: IntegralAlgebra,
                T_prime: OrderedSet[IntegralPolynomial],
                E: OrderedSet[sp.Function, sp.Function, IntegralPolynomial]
                ) -> tuple:
    """
    Algorithm 4
    output T_E and E'
    """
    T_E = OrderedSet()
    E_prime = OrderedSet([elem for elem in E])
    t = IA.t
    for P in T_prime:
        temp = IA.find_A_A0_G_F(P)
        if temp != None:
            A, A0, G, F = temp
            int_G = IA.integrate_polynomial(G)
            # this code is a bit different than algo 4
            # this allow to not introduce an encoding of an exp
            # that is already in E_prime 
            int_G = IA.reduce(int_G, T_prime)[0] 
            
            # check that int G != from all Q_i in Eprime
            check = [
                    IA.polynomials_subtraction(int_G, Q_i).is_zero() 
                    for _, _, Q_i in E_prime
                    ]
            
            if not any(check):
                k = len(E_prime) + 1
                uk = sp.Function(f"u{k}")
                vk = sp.Function(f"v{k}")
                new_item = (uk(t), vk(t), int_G)
                E_prime.add(new_item)
                uk_pol = IntegralPolynomial(IM(uk(t)))
                vk_pol = IntegralPolynomial(IM(vk(t)))
            else: 
                index_True_in_check = [ 
                                        i for i in range(len(check)) 
                                        if check[i] is True
                                      ][0]
                uk,vk,_ = list(E_prime)[index_True_in_check]
                uk_pol = IntegralPolynomial(IM(uk))
                vk_pol = IntegralPolynomial(IM(vk))
            # then, we compoute P_exp = A - (A0 u_k + u_k \int (v_k F))
            # from right to left
            
            temp = IA.integrate_polynomial(IA.polynomials_product(vk_pol, F))
            temp = IA.polynomials_product(uk_pol,temp)
            temp = IA.polynomials_add(IA.polynomials_product(A0,uk_pol), temp)
            P_exp = IA.polynomials_subtraction(A, temp)
            if not P_exp.is_zero():
                T_E.add(P_exp)

    return T_E, E_prime
 
def extend_X_with_exp(IA: IntegralAlgebra,
                    E: OrderedSet[sp.Function, sp.Function, IntegralPolynomial]
                    ) -> list:
    """
    Algorithm 5
    Here, X is inside the IntegralAlgebra object (self.order)
    We will return a modified X and replace the self.used_order 
    after this function call to update self.IMO_le according to
    the new X'
    """
    # If needed, reorder E such that each Qi does not involve any 
    # uj or vj with j > i. This can be done by a topological sort.

    # print("WARNING: topological sort not implemented")

    X_prime = IA.order
    
    for ui,vi,Qi in E: # = for i from 1 to m
        if expr_has_symbols(Qi.get_sympy_repr(), X_prime):
            indeterminates = Qi.get_time_dependant_functions()
            greatest_inds = None

            #from left (greatest) to right
            for inds, k in zip(X_prime, range(len(X_prime))): 
                if inds in indeterminates:
                    greatest_inds = inds
                    X_prime = X_prime[:k] + [ui,vi] + X_prime[k:]
                    break;
            assert greatest_inds is not None
        else:
            X_prime = X_prime + [ui, vi]
    return X_prime