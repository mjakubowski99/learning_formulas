#include "FormulaCrosser.hpp"

class OnePointCrosser : public FormulaCrosser {
    public:
        Formula cross(Formula & a, Formula & b);
    private:
        Formula run(Formula & a, Formula & b);
};