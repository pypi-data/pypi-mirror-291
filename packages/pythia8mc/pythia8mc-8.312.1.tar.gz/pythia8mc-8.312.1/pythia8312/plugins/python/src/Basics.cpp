#include <Pythia8/Basics.h>
#include <cwchar>
#include <ios>
#include <locale>
#include <ostream>
#include <sstream> // __str__
#include <streambuf>
#include <string>
#include <utility>

#include <pybind11/pybind11.h>
#include <functional>
#include <string>
#include <Pythia8/UserHooks.h>
#include <Pythia8/SplittingsOnia.h>
#include <Pythia8/HeavyIons.h>
#include <Pythia8/BeamShape.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

// Pythia8::RndmEngine file:Pythia8/Basics.h line:353
struct PyCallBack_Pythia8_RndmEngine : public Pythia8::RndmEngine {
	using Pythia8::RndmEngine::RndmEngine;

	double flat() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RndmEngine *>(this), "flat");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return RndmEngine::flat();
	}
};

void bind_Pythia8_Basics(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	// Pythia8::dot3(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:158
	M("Pythia8").def("dot3", (double (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::dot3, "C++: Pythia8::dot3(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> double", pybind11::arg("v1"), pybind11::arg("v2"));

	// Pythia8::cross3(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:159
	M("Pythia8").def("cross3", (class Pythia8::Vec4 (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::cross3, "C++: Pythia8::cross3(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> class Pythia8::Vec4", pybind11::arg("v1"), pybind11::arg("v2"));

	// Pythia8::cross4(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:162
	M("Pythia8").def("cross4", (class Pythia8::Vec4 (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::cross4, "C++: Pythia8::cross4(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> class Pythia8::Vec4", pybind11::arg("a"), pybind11::arg("b"), pybind11::arg("c"));

	// Pythia8::theta(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:165
	M("Pythia8").def("theta", (double (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::theta, "C++: Pythia8::theta(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> double", pybind11::arg("v1"), pybind11::arg("v2"));

	// Pythia8::costheta(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:166
	M("Pythia8").def("costheta", (double (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::costheta, "C++: Pythia8::costheta(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> double", pybind11::arg("v1"), pybind11::arg("v2"));

	// Pythia8::phi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:169
	M("Pythia8").def("phi", (double (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::phi, "C++: Pythia8::phi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> double", pybind11::arg("v1"), pybind11::arg("v2"));

	// Pythia8::cosphi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:170
	M("Pythia8").def("cosphi", (double (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::cosphi, "C++: Pythia8::cosphi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> double", pybind11::arg("v1"), pybind11::arg("v2"));

	// Pythia8::phi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:173
	M("Pythia8").def("phi", (double (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::phi, "C++: Pythia8::phi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> double", pybind11::arg("v1"), pybind11::arg("v2"), pybind11::arg("n"));

	// Pythia8::cosphi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:174
	M("Pythia8").def("cosphi", (double (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::cosphi, "C++: Pythia8::cosphi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> double", pybind11::arg("v1"), pybind11::arg("v2"), pybind11::arg("n"));

	// Pythia8::RRapPhi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:177
	M("Pythia8").def("RRapPhi", (double (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::RRapPhi, "C++: Pythia8::RRapPhi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> double", pybind11::arg("v1"), pybind11::arg("v2"));

	// Pythia8::REtaPhi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:178
	M("Pythia8").def("REtaPhi", (double (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::REtaPhi, "C++: Pythia8::REtaPhi(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> double", pybind11::arg("v1"), pybind11::arg("v2"));

	// Pythia8::pShift(class Pythia8::Vec4 &, class Pythia8::Vec4 &, double, double) file:Pythia8/Basics.h line:181
	M("Pythia8").def("pShift", (bool (*)(class Pythia8::Vec4 &, class Pythia8::Vec4 &, double, double)) &Pythia8::pShift, "C++: Pythia8::pShift(class Pythia8::Vec4 &, class Pythia8::Vec4 &, double, double) --> bool", pybind11::arg("p1Move"), pybind11::arg("p2Move"), pybind11::arg("m1New"), pybind11::arg("m2New"));

	// Pythia8::getTwoPerpendicular(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:184
	M("Pythia8").def("getTwoPerpendicular", (struct std::pair<class Pythia8::Vec4, class Pythia8::Vec4> (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::getTwoPerpendicular, "C++: Pythia8::getTwoPerpendicular(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> struct std::pair<class Pythia8::Vec4, class Pythia8::Vec4>", pybind11::arg("v1"), pybind11::arg("v2"));

	// Pythia8::costheta(double, double, double, double, double) file:Pythia8/Basics.h line:223
	M("Pythia8").def("costheta", (double (*)(double, double, double, double, double)) &Pythia8::costheta, "C++: Pythia8::costheta(double, double, double, double, double) --> double", pybind11::arg("e1"), pybind11::arg("e2"), pybind11::arg("m1"), pybind11::arg("m2"), pybind11::arg("s12"));

	{ // Pythia8::RotBstMatrix file:Pythia8/Basics.h line:252
		pybind11::class_<Pythia8::RotBstMatrix, std::shared_ptr<Pythia8::RotBstMatrix>> cl(M("Pythia8"), "RotBstMatrix", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::RotBstMatrix(); } ) );
		cl.def( pybind11::init( [](Pythia8::RotBstMatrix const &o){ return new Pythia8::RotBstMatrix(o); } ) );
		cl.def("assign", (class Pythia8::RotBstMatrix & (Pythia8::RotBstMatrix::*)(const class Pythia8::RotBstMatrix &)) &Pythia8::RotBstMatrix::operator=, "C++: Pythia8::RotBstMatrix::operator=(const class Pythia8::RotBstMatrix &) --> class Pythia8::RotBstMatrix &", pybind11::return_value_policy::reference, pybind11::arg("Min"));
		cl.def("rot", [](Pythia8::RotBstMatrix &o) -> void { return o.rot(); }, "");
		cl.def("rot", [](Pythia8::RotBstMatrix &o, double const & a0) -> void { return o.rot(a0); }, "", pybind11::arg(""));
		cl.def("rot", (void (Pythia8::RotBstMatrix::*)(double, double)) &Pythia8::RotBstMatrix::rot, "C++: Pythia8::RotBstMatrix::rot(double, double) --> void", pybind11::arg(""), pybind11::arg(""));
		cl.def("rot", (void (Pythia8::RotBstMatrix::*)(const class Pythia8::Vec4 &)) &Pythia8::RotBstMatrix::rot, "C++: Pythia8::RotBstMatrix::rot(const class Pythia8::Vec4 &) --> void", pybind11::arg("p"));
		cl.def("bst", [](Pythia8::RotBstMatrix &o) -> void { return o.bst(); }, "");
		cl.def("bst", [](Pythia8::RotBstMatrix &o, double const & a0) -> void { return o.bst(a0); }, "", pybind11::arg(""));
		cl.def("bst", [](Pythia8::RotBstMatrix &o, double const & a0, double const & a1) -> void { return o.bst(a0, a1); }, "", pybind11::arg(""), pybind11::arg(""));
		cl.def("bst", (void (Pythia8::RotBstMatrix::*)(double, double, double)) &Pythia8::RotBstMatrix::bst, "C++: Pythia8::RotBstMatrix::bst(double, double, double) --> void", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("bst", (void (Pythia8::RotBstMatrix::*)(const class Pythia8::Vec4 &)) &Pythia8::RotBstMatrix::bst, "C++: Pythia8::RotBstMatrix::bst(const class Pythia8::Vec4 &) --> void", pybind11::arg(""));
		cl.def("bstback", (void (Pythia8::RotBstMatrix::*)(const class Pythia8::Vec4 &)) &Pythia8::RotBstMatrix::bstback, "C++: Pythia8::RotBstMatrix::bstback(const class Pythia8::Vec4 &) --> void", pybind11::arg(""));
		cl.def("bst", (void (Pythia8::RotBstMatrix::*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::RotBstMatrix::bst, "C++: Pythia8::RotBstMatrix::bst(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> void", pybind11::arg(""), pybind11::arg(""));
		cl.def("toCMframe", (void (Pythia8::RotBstMatrix::*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::RotBstMatrix::toCMframe, "C++: Pythia8::RotBstMatrix::toCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> void", pybind11::arg(""), pybind11::arg(""));
		cl.def("fromCMframe", [](Pythia8::RotBstMatrix &o, const class Pythia8::Vec4 & a0, const class Pythia8::Vec4 & a1) -> void { return o.fromCMframe(a0, a1); }, "", pybind11::arg(""), pybind11::arg(""));
		cl.def("fromCMframe", (void (Pythia8::RotBstMatrix::*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, bool)) &Pythia8::RotBstMatrix::fromCMframe, "C++: Pythia8::RotBstMatrix::fromCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, bool) --> void", pybind11::arg(""), pybind11::arg(""), pybind11::arg("flip"));
		cl.def("toSameVframe", (void (Pythia8::RotBstMatrix::*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::RotBstMatrix::toSameVframe, "C++: Pythia8::RotBstMatrix::toSameVframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> void", pybind11::arg(""), pybind11::arg(""));
		cl.def("fromSameVframe", (void (Pythia8::RotBstMatrix::*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::RotBstMatrix::fromSameVframe, "C++: Pythia8::RotBstMatrix::fromSameVframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> void", pybind11::arg(""), pybind11::arg(""));
		cl.def("rotbst", (void (Pythia8::RotBstMatrix::*)(const class Pythia8::RotBstMatrix &)) &Pythia8::RotBstMatrix::rotbst, "C++: Pythia8::RotBstMatrix::rotbst(const class Pythia8::RotBstMatrix &) --> void", pybind11::arg(""));
		cl.def("invert", (void (Pythia8::RotBstMatrix::*)()) &Pythia8::RotBstMatrix::invert, "C++: Pythia8::RotBstMatrix::invert() --> void");
		cl.def("inverse", (class Pythia8::RotBstMatrix (Pythia8::RotBstMatrix::*)() const) &Pythia8::RotBstMatrix::inverse, "C++: Pythia8::RotBstMatrix::inverse() const --> class Pythia8::RotBstMatrix");
		cl.def("reset", (void (Pythia8::RotBstMatrix::*)()) &Pythia8::RotBstMatrix::reset, "C++: Pythia8::RotBstMatrix::reset() --> void");
		cl.def("value", (double (Pythia8::RotBstMatrix::*)(int, int)) &Pythia8::RotBstMatrix::value, "C++: Pythia8::RotBstMatrix::value(int, int) --> double", pybind11::arg("i"), pybind11::arg("j"));
		cl.def("deviation", (double (Pythia8::RotBstMatrix::*)() const) &Pythia8::RotBstMatrix::deviation, "C++: Pythia8::RotBstMatrix::deviation() const --> double");
		cl.def("__mul__", (class Pythia8::Vec4 (Pythia8::RotBstMatrix::*)(class Pythia8::Vec4) const) &Pythia8::RotBstMatrix::operator*, "C++: Pythia8::RotBstMatrix::operator*(class Pythia8::Vec4) const --> class Pythia8::Vec4", pybind11::arg("p"));
		cl.def("__mul__", (class Pythia8::RotBstMatrix (Pythia8::RotBstMatrix::*)(class Pythia8::RotBstMatrix) const) &Pythia8::RotBstMatrix::operator*, "C++: Pythia8::RotBstMatrix::operator*(class Pythia8::RotBstMatrix) const --> class Pythia8::RotBstMatrix", pybind11::arg("R"));

		cl.def("__str__", [](Pythia8::RotBstMatrix const &o) -> std::string { std::ostringstream s; s << o; return s.str(); } );
	}
	// Pythia8::toCMframe(const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:317
	M("Pythia8").def("toCMframe", (class Pythia8::RotBstMatrix (*)(const class Pythia8::Vec4 &)) &Pythia8::toCMframe, "C++: Pythia8::toCMframe(const class Pythia8::Vec4 &) --> class Pythia8::RotBstMatrix", pybind11::arg("p"));

	// Pythia8::fromCMframe(const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:321
	M("Pythia8").def("fromCMframe", (class Pythia8::RotBstMatrix (*)(const class Pythia8::Vec4 &)) &Pythia8::fromCMframe, "C++: Pythia8::fromCMframe(const class Pythia8::Vec4 &) --> class Pythia8::RotBstMatrix", pybind11::arg("p"));

	// Pythia8::toCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:326
	M("Pythia8").def("toCMframe", (class Pythia8::RotBstMatrix (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::toCMframe, "C++: Pythia8::toCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> class Pythia8::RotBstMatrix", pybind11::arg("p1"), pybind11::arg("p2"));

	// Pythia8::fromCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, bool) file:Pythia8/Basics.h line:332
	M("Pythia8").def("fromCMframe", [](const class Pythia8::Vec4 & a0, const class Pythia8::Vec4 & a1) -> Pythia8::RotBstMatrix { return Pythia8::fromCMframe(a0, a1); }, "", pybind11::arg("p1"), pybind11::arg("p2"));
	M("Pythia8").def("fromCMframe", (class Pythia8::RotBstMatrix (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, bool)) &Pythia8::fromCMframe, "C++: Pythia8::fromCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, bool) --> class Pythia8::RotBstMatrix", pybind11::arg("p1"), pybind11::arg("p2"), pybind11::arg("flip"));

	// Pythia8::toCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:338
	M("Pythia8").def("toCMframe", (class Pythia8::RotBstMatrix (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::toCMframe, "C++: Pythia8::toCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> class Pythia8::RotBstMatrix", pybind11::arg("ptot"), pybind11::arg("pz"), pybind11::arg("pxz"));

	// Pythia8::fromCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) file:Pythia8/Basics.h line:345
	M("Pythia8").def("fromCMframe", (class Pythia8::RotBstMatrix (*)(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &)) &Pythia8::fromCMframe, "C++: Pythia8::fromCMframe(const class Pythia8::Vec4 &, const class Pythia8::Vec4 &, const class Pythia8::Vec4 &) --> class Pythia8::RotBstMatrix", pybind11::arg("ptot"), pybind11::arg("pz"), pybind11::arg("pxz"));

	{ // Pythia8::RndmEngine file:Pythia8/Basics.h line:353
		pybind11::class_<Pythia8::RndmEngine, std::shared_ptr<Pythia8::RndmEngine>, PyCallBack_Pythia8_RndmEngine> cl(M("Pythia8"), "RndmEngine", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](PyCallBack_Pythia8_RndmEngine const &o){ return new PyCallBack_Pythia8_RndmEngine(o); } ) );
		cl.def( pybind11::init( [](Pythia8::RndmEngine const &o){ return new Pythia8::RndmEngine(o); } ) );
		cl.def( pybind11::init( [](){ return new Pythia8::RndmEngine(); }, [](){ return new PyCallBack_Pythia8_RndmEngine(); } ) );
		cl.def("flat", (double (Pythia8::RndmEngine::*)()) &Pythia8::RndmEngine::flat, "C++: Pythia8::RndmEngine::flat() --> double");
		cl.def("assign", (class Pythia8::RndmEngine & (Pythia8::RndmEngine::*)(const class Pythia8::RndmEngine &)) &Pythia8::RndmEngine::operator=, "C++: Pythia8::RndmEngine::operator=(const class Pythia8::RndmEngine &) --> class Pythia8::RndmEngine &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::RndmState file:Pythia8/Basics.h line:371
		pybind11::class_<Pythia8::RndmState, std::shared_ptr<Pythia8::RndmState>> cl(M("Pythia8"), "RndmState", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](Pythia8::RndmState const &o){ return new Pythia8::RndmState(o); } ) );
		cl.def( pybind11::init( [](){ return new Pythia8::RndmState(); } ) );
		cl.def_readwrite("i97", &Pythia8::RndmState::i97);
		cl.def_readwrite("j97", &Pythia8::RndmState::j97);
		cl.def_readwrite("seed", &Pythia8::RndmState::seed);
		cl.def_readwrite("sequence", &Pythia8::RndmState::sequence);
		cl.def_readwrite("c", &Pythia8::RndmState::c);
		cl.def_readwrite("cd", &Pythia8::RndmState::cd);
		cl.def_readwrite("cm", &Pythia8::RndmState::cm);
		cl.def("__eq__", (bool (Pythia8::RndmState::*)(const struct Pythia8::RndmState &) const) &Pythia8::RndmState::operator==, "C++: Pythia8::RndmState::operator==(const struct Pythia8::RndmState &) const --> bool", pybind11::arg("other"));
		cl.def("assign", (struct Pythia8::RndmState & (Pythia8::RndmState::*)(const struct Pythia8::RndmState &)) &Pythia8::RndmState::operator=, "C++: Pythia8::RndmState::operator=(const struct Pythia8::RndmState &) --> struct Pythia8::RndmState &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
}
