#include <Pythia8/Basics.h>
#include <Pythia8/BeamSetup.h>
#include <Pythia8/Event.h>
#include <Pythia8/FragmentationFlavZpT.h>
#include <Pythia8/FragmentationSystems.h>
#include <Pythia8/HadronWidths.h>
#include <Pythia8/Info.h>
#include <Pythia8/LHEF3.h>
#include <Pythia8/Logger.h>
#include <Pythia8/NucleonExcitations.h>
#include <Pythia8/ParticleData.h>
#include <Pythia8/PartonSystems.h>
#include <Pythia8/PhysicsBase.h>
#include <Pythia8/ResonanceWidths.h>
#include <Pythia8/Ropewalk.h>
#include <Pythia8/Settings.h>
#include <Pythia8/SigmaLowEnergy.h>
#include <Pythia8/SigmaTotal.h>
#include <Pythia8/StandardModel.h>
#include <Pythia8/StringInteractions.h>
#include <Pythia8/SusyCouplings.h>
#include <Pythia8/Weights.h>
#include <cwchar>
#include <functional>
#include <ios>
#include <istream>
#include <iterator>
#include <map>
#include <memory>
#include <ostream>
#include <sstream> // __str__
#include <streambuf>
#include <string>
#include <utility>
#include <vector>

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

// Pythia8::Ropewalk file:Pythia8/Ropewalk.h line:211
struct PyCallBack_Pythia8_Ropewalk : public Pythia8::Ropewalk {
	using Pythia8::Ropewalk::Ropewalk;

	bool init() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::Ropewalk *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return Ropewalk::init();
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::Ropewalk *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::Ropewalk *>(this), "onBeginEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onBeginEvent();
	}
	void onEndEvent(enum Pythia8::PhysicsBase::Status a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::Ropewalk *>(this), "onEndEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onEndEvent(a0);
	}
	void onStat() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::Ropewalk *>(this), "onStat");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onStat();
	}
};

// Pythia8::RopeFragPars file:Pythia8/Ropewalk.h line:304
struct PyCallBack_Pythia8_RopeFragPars : public Pythia8::RopeFragPars {
	using Pythia8::RopeFragPars::RopeFragPars;

	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopeFragPars *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopeFragPars *>(this), "onBeginEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onBeginEvent();
	}
	void onEndEvent(enum Pythia8::PhysicsBase::Status a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopeFragPars *>(this), "onEndEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onEndEvent(a0);
	}
	void onStat() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopeFragPars *>(this), "onStat");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onStat();
	}
};

// Pythia8::FlavourRope file:Pythia8/Ropewalk.h line:374
struct PyCallBack_Pythia8_FlavourRope : public Pythia8::FlavourRope {
	using Pythia8::FlavourRope::FlavourRope;

	bool init() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FlavourRope *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return FlavourRope::init();
	}
	bool doChangeFragPar(class Pythia8::StringFlav * a0, class Pythia8::StringZ * a1, class Pythia8::StringPT * a2, double a3, class std::vector<int, class std::allocator<int> > a4, int a5) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FlavourRope *>(this), "doChangeFragPar");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4, a5);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return FlavourRope::doChangeFragPar(a0, a1, a2, a3, a4, a5);
	}
	bool initEvent(class Pythia8::Event & a0, class Pythia8::ColConfig & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FlavourRope *>(this), "initEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return FlavourRope::initEvent(a0, a1);
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FlavourRope *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return FlavourRope::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FlavourRope *>(this), "onBeginEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onBeginEvent();
	}
	void onEndEvent(enum Pythia8::PhysicsBase::Status a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FlavourRope *>(this), "onEndEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onEndEvent(a0);
	}
	void onStat() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FlavourRope *>(this), "onStat");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onStat();
	}
};

// Pythia8::RopewalkShover file:Pythia8/Ropewalk.h line:457
struct PyCallBack_Pythia8_RopewalkShover : public Pythia8::RopewalkShover {
	using Pythia8::RopewalkShover::RopewalkShover;

	bool stringRepulsion(class Pythia8::Event & a0, class Pythia8::ColConfig & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopewalkShover *>(this), "stringRepulsion");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return RopewalkShover::stringRepulsion(a0, a1);
	}
	bool init() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopewalkShover *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return StringRepulsionBase::init();
	}
	bool hadronRepulsion(class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopewalkShover *>(this), "hadronRepulsion");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return StringRepulsionBase::hadronRepulsion(a0);
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopewalkShover *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopewalkShover *>(this), "onBeginEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onBeginEvent();
	}
	void onEndEvent(enum Pythia8::PhysicsBase::Status a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopewalkShover *>(this), "onEndEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onEndEvent(a0);
	}
	void onStat() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RopewalkShover *>(this), "onStat");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onStat();
	}
};

// Pythia8::NucleonExcitations file:Pythia8/NucleonExcitations.h line:23
struct PyCallBack_Pythia8_NucleonExcitations : public Pythia8::NucleonExcitations {
	using Pythia8::NucleonExcitations::NucleonExcitations;

	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::NucleonExcitations *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::NucleonExcitations *>(this), "onBeginEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onBeginEvent();
	}
	void onEndEvent(enum Pythia8::PhysicsBase::Status a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::NucleonExcitations *>(this), "onEndEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onEndEvent(a0);
	}
	void onStat() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::NucleonExcitations *>(this), "onStat");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onStat();
	}
};

void bind_Pythia8_Ropewalk(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // Pythia8::Ropewalk file:Pythia8/Ropewalk.h line:211
		pybind11::class_<Pythia8::Ropewalk, std::shared_ptr<Pythia8::Ropewalk>, PyCallBack_Pythia8_Ropewalk, Pythia8::StringInteractions> cl(M("Pythia8"), "Ropewalk", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::Ropewalk(); }, [](){ return new PyCallBack_Pythia8_Ropewalk(); } ) );
		cl.def("init", (bool (Pythia8::Ropewalk::*)()) &Pythia8::Ropewalk::init, "C++: Pythia8::Ropewalk::init() --> bool");
		cl.def("extractDipoles", (bool (Pythia8::Ropewalk::*)(class Pythia8::Event &, class Pythia8::ColConfig &)) &Pythia8::Ropewalk::extractDipoles, "C++: Pythia8::Ropewalk::extractDipoles(class Pythia8::Event &, class Pythia8::ColConfig &) --> bool", pybind11::arg("event"), pybind11::arg("colConfig"));
		cl.def("calculateOverlaps", (bool (Pythia8::Ropewalk::*)()) &Pythia8::Ropewalk::calculateOverlaps, "C++: Pythia8::Ropewalk::calculateOverlaps() --> bool");
		cl.def("getKappaHere", (double (Pythia8::Ropewalk::*)(int, int, double)) &Pythia8::Ropewalk::getKappaHere, "C++: Pythia8::Ropewalk::getKappaHere(int, int, double) --> double", pybind11::arg("e1"), pybind11::arg("e2"), pybind11::arg("yfrac"));
		cl.def("multiplicity", (double (Pythia8::Ropewalk::*)(double, double)) &Pythia8::Ropewalk::multiplicity, "C++: Pythia8::Ropewalk::multiplicity(double, double) --> double", pybind11::arg("p"), pybind11::arg("q"));
		cl.def("averageKappa", (double (Pythia8::Ropewalk::*)()) &Pythia8::Ropewalk::averageKappa, "C++: Pythia8::Ropewalk::averageKappa() --> double");
		cl.def("select", (struct std::pair<int, int> (Pythia8::Ropewalk::*)(int, int, class Pythia8::Rndm *)) &Pythia8::Ropewalk::select, "C++: Pythia8::Ropewalk::select(int, int, class Pythia8::Rndm *) --> struct std::pair<int, int>", pybind11::arg("m"), pybind11::arg("n"), pybind11::arg("rndm"));
		cl.def("shoveTheDipoles", (void (Pythia8::Ropewalk::*)(class Pythia8::Event &)) &Pythia8::Ropewalk::shoveTheDipoles, "C++: Pythia8::Ropewalk::shoveTheDipoles(class Pythia8::Event &) --> void", pybind11::arg("event"));
	}
	{ // Pythia8::RopeFragPars file:Pythia8/Ropewalk.h line:304
		pybind11::class_<Pythia8::RopeFragPars, std::shared_ptr<Pythia8::RopeFragPars>, PyCallBack_Pythia8_RopeFragPars, Pythia8::PhysicsBase> cl(M("Pythia8"), "RopeFragPars", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::RopeFragPars(); }, [](){ return new PyCallBack_Pythia8_RopeFragPars(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_RopeFragPars const &o){ return new PyCallBack_Pythia8_RopeFragPars(o); } ) );
		cl.def( pybind11::init( [](Pythia8::RopeFragPars const &o){ return new Pythia8::RopeFragPars(o); } ) );
		cl.def("init", (bool (Pythia8::RopeFragPars::*)()) &Pythia8::RopeFragPars::init, "C++: Pythia8::RopeFragPars::init() --> bool");
		cl.def("getEffectiveParameters", (class std::map<std::string, double, struct std::less<std::string >, class std::allocator<struct std::pair<const std::string, double> > > (Pythia8::RopeFragPars::*)(double)) &Pythia8::RopeFragPars::getEffectiveParameters, "C++: Pythia8::RopeFragPars::getEffectiveParameters(double) --> class std::map<std::string, double, struct std::less<std::string >, class std::allocator<struct std::pair<const std::string, double> > >", pybind11::arg("h"));
		cl.def("assign", (class Pythia8::RopeFragPars & (Pythia8::RopeFragPars::*)(const class Pythia8::RopeFragPars &)) &Pythia8::RopeFragPars::operator=, "C++: Pythia8::RopeFragPars::operator=(const class Pythia8::RopeFragPars &) --> class Pythia8::RopeFragPars &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::FlavourRope file:Pythia8/Ropewalk.h line:374
		pybind11::class_<Pythia8::FlavourRope, std::shared_ptr<Pythia8::FlavourRope>, PyCallBack_Pythia8_FlavourRope, Pythia8::FragmentationModifierBase> cl(M("Pythia8"), "FlavourRope", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init<class Pythia8::Ropewalk &>(), pybind11::arg("rwIn") );

		cl.def("init", (bool (Pythia8::FlavourRope::*)()) &Pythia8::FlavourRope::init, "C++: Pythia8::FlavourRope::init() --> bool");
		cl.def("doChangeFragPar", (bool (Pythia8::FlavourRope::*)(class Pythia8::StringFlav *, class Pythia8::StringZ *, class Pythia8::StringPT *, double, class std::vector<int, class std::allocator<int> >, int)) &Pythia8::FlavourRope::doChangeFragPar, "C++: Pythia8::FlavourRope::doChangeFragPar(class Pythia8::StringFlav *, class Pythia8::StringZ *, class Pythia8::StringPT *, double, class std::vector<int, class std::allocator<int> >, int) --> bool", pybind11::arg("flavPtr"), pybind11::arg("zPtr"), pybind11::arg("pTPtr"), pybind11::arg("m2Had"), pybind11::arg("iParton"), pybind11::arg("endId"));
		cl.def("setEnhancement", (void (Pythia8::FlavourRope::*)(double)) &Pythia8::FlavourRope::setEnhancement, "C++: Pythia8::FlavourRope::setEnhancement(double) --> void", pybind11::arg("hIn"));
		cl.def("setEventPtr", (void (Pythia8::FlavourRope::*)(class Pythia8::Event &)) &Pythia8::FlavourRope::setEventPtr, "C++: Pythia8::FlavourRope::setEventPtr(class Pythia8::Event &) --> void", pybind11::arg("event"));
		cl.def("initEvent", (bool (Pythia8::FlavourRope::*)(class Pythia8::Event &, class Pythia8::ColConfig &)) &Pythia8::FlavourRope::initEvent, "C++: Pythia8::FlavourRope::initEvent(class Pythia8::Event &, class Pythia8::ColConfig &) --> bool", pybind11::arg("event"), pybind11::arg("colConfig"));
		cl.def("onInitInfoPtr", (void (Pythia8::FlavourRope::*)()) &Pythia8::FlavourRope::onInitInfoPtr, "C++: Pythia8::FlavourRope::onInitInfoPtr() --> void");
		cl.def("assign", (class Pythia8::FlavourRope & (Pythia8::FlavourRope::*)(const class Pythia8::FlavourRope &)) &Pythia8::FlavourRope::operator=, "C++: Pythia8::FlavourRope::operator=(const class Pythia8::FlavourRope &) --> class Pythia8::FlavourRope &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::RopewalkShover file:Pythia8/Ropewalk.h line:457
		pybind11::class_<Pythia8::RopewalkShover, std::shared_ptr<Pythia8::RopewalkShover>, PyCallBack_Pythia8_RopewalkShover, Pythia8::StringRepulsionBase> cl(M("Pythia8"), "RopewalkShover", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init<class Pythia8::Ropewalk &>(), pybind11::arg("rwIn") );

		cl.def("stringRepulsion", (bool (Pythia8::RopewalkShover::*)(class Pythia8::Event &, class Pythia8::ColConfig &)) &Pythia8::RopewalkShover::stringRepulsion, "C++: Pythia8::RopewalkShover::stringRepulsion(class Pythia8::Event &, class Pythia8::ColConfig &) --> bool", pybind11::arg("event"), pybind11::arg("colConfig"));
		cl.def("assign", (class Pythia8::RopewalkShover & (Pythia8::RopewalkShover::*)(const class Pythia8::RopewalkShover &)) &Pythia8::RopewalkShover::operator=, "C++: Pythia8::RopewalkShover::operator=(const class Pythia8::RopewalkShover &) --> class Pythia8::RopewalkShover &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::PartonSystem file:Pythia8/PartonSystems.h line:22
		pybind11::class_<Pythia8::PartonSystem, std::shared_ptr<Pythia8::PartonSystem>> cl(M("Pythia8"), "PartonSystem", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::PartonSystem(); } ) );
		cl.def( pybind11::init( [](Pythia8::PartonSystem const &o){ return new Pythia8::PartonSystem(o); } ) );
		cl.def_readwrite("hard", &Pythia8::PartonSystem::hard);
		cl.def_readwrite("iInA", &Pythia8::PartonSystem::iInA);
		cl.def_readwrite("iInB", &Pythia8::PartonSystem::iInB);
		cl.def_readwrite("iInRes", &Pythia8::PartonSystem::iInRes);
		cl.def_readwrite("iOut", &Pythia8::PartonSystem::iOut);
		cl.def_readwrite("sHat", &Pythia8::PartonSystem::sHat);
		cl.def_readwrite("pTHat", &Pythia8::PartonSystem::pTHat);
		cl.def("assign", (class Pythia8::PartonSystem & (Pythia8::PartonSystem::*)(const class Pythia8::PartonSystem &)) &Pythia8::PartonSystem::operator=, "C++: Pythia8::PartonSystem::operator=(const class Pythia8::PartonSystem &) --> class Pythia8::PartonSystem &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::PartonSystems file:Pythia8/PartonSystems.h line:42
		pybind11::class_<Pythia8::PartonSystems, std::shared_ptr<Pythia8::PartonSystems>> cl(M("Pythia8"), "PartonSystems", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::PartonSystems(); } ) );
		cl.def( pybind11::init( [](Pythia8::PartonSystems const &o){ return new Pythia8::PartonSystems(o); } ) );
		cl.def("clear", (void (Pythia8::PartonSystems::*)()) &Pythia8::PartonSystems::clear, "C++: Pythia8::PartonSystems::clear() --> void");
		cl.def("addSys", (int (Pythia8::PartonSystems::*)()) &Pythia8::PartonSystems::addSys, "C++: Pythia8::PartonSystems::addSys() --> int");
		cl.def("sizeSys", (int (Pythia8::PartonSystems::*)() const) &Pythia8::PartonSystems::sizeSys, "C++: Pythia8::PartonSystems::sizeSys() const --> int");
		cl.def("setHard", (void (Pythia8::PartonSystems::*)(int, bool)) &Pythia8::PartonSystems::setHard, "C++: Pythia8::PartonSystems::setHard(int, bool) --> void", pybind11::arg("iSys"), pybind11::arg("hard"));
		cl.def("setInA", (void (Pythia8::PartonSystems::*)(int, int)) &Pythia8::PartonSystems::setInA, "C++: Pythia8::PartonSystems::setInA(int, int) --> void", pybind11::arg("iSys"), pybind11::arg("iPos"));
		cl.def("setInB", (void (Pythia8::PartonSystems::*)(int, int)) &Pythia8::PartonSystems::setInB, "C++: Pythia8::PartonSystems::setInB(int, int) --> void", pybind11::arg("iSys"), pybind11::arg("iPos"));
		cl.def("setInRes", (void (Pythia8::PartonSystems::*)(int, int)) &Pythia8::PartonSystems::setInRes, "C++: Pythia8::PartonSystems::setInRes(int, int) --> void", pybind11::arg("iSys"), pybind11::arg("iPos"));
		cl.def("addOut", (void (Pythia8::PartonSystems::*)(int, int)) &Pythia8::PartonSystems::addOut, "C++: Pythia8::PartonSystems::addOut(int, int) --> void", pybind11::arg("iSys"), pybind11::arg("iPos"));
		cl.def("popBackOut", (void (Pythia8::PartonSystems::*)(int)) &Pythia8::PartonSystems::popBackOut, "C++: Pythia8::PartonSystems::popBackOut(int) --> void", pybind11::arg("iSys"));
		cl.def("setOut", (void (Pythia8::PartonSystems::*)(int, int, int)) &Pythia8::PartonSystems::setOut, "C++: Pythia8::PartonSystems::setOut(int, int, int) --> void", pybind11::arg("iSys"), pybind11::arg("iMem"), pybind11::arg("iPos"));
		cl.def("replace", (void (Pythia8::PartonSystems::*)(int, int, int)) &Pythia8::PartonSystems::replace, "C++: Pythia8::PartonSystems::replace(int, int, int) --> void", pybind11::arg("iSys"), pybind11::arg("iPosOld"), pybind11::arg("iPosNew"));
		cl.def("setSHat", (void (Pythia8::PartonSystems::*)(int, double)) &Pythia8::PartonSystems::setSHat, "C++: Pythia8::PartonSystems::setSHat(int, double) --> void", pybind11::arg("iSys"), pybind11::arg("sHatIn"));
		cl.def("setPTHat", (void (Pythia8::PartonSystems::*)(int, double)) &Pythia8::PartonSystems::setPTHat, "C++: Pythia8::PartonSystems::setPTHat(int, double) --> void", pybind11::arg("iSys"), pybind11::arg("pTHatIn"));
		cl.def("setSizeSys", (void (Pythia8::PartonSystems::*)(int)) &Pythia8::PartonSystems::setSizeSys, "C++: Pythia8::PartonSystems::setSizeSys(int) --> void", pybind11::arg("iSize"));
		cl.def("hasInAB", (bool (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::hasInAB, "C++: Pythia8::PartonSystems::hasInAB(int) const --> bool", pybind11::arg("iSys"));
		cl.def("hasInRes", (bool (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::hasInRes, "C++: Pythia8::PartonSystems::hasInRes(int) const --> bool", pybind11::arg("iSys"));
		cl.def("getHard", (bool (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::getHard, "C++: Pythia8::PartonSystems::getHard(int) const --> bool", pybind11::arg("iSys"));
		cl.def("getInA", (int (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::getInA, "C++: Pythia8::PartonSystems::getInA(int) const --> int", pybind11::arg("iSys"));
		cl.def("getInB", (int (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::getInB, "C++: Pythia8::PartonSystems::getInB(int) const --> int", pybind11::arg("iSys"));
		cl.def("getInRes", (int (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::getInRes, "C++: Pythia8::PartonSystems::getInRes(int) const --> int", pybind11::arg("iSys"));
		cl.def("sizeOut", (int (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::sizeOut, "C++: Pythia8::PartonSystems::sizeOut(int) const --> int", pybind11::arg("iSys"));
		cl.def("getOut", (int (Pythia8::PartonSystems::*)(int, int) const) &Pythia8::PartonSystems::getOut, "C++: Pythia8::PartonSystems::getOut(int, int) const --> int", pybind11::arg("iSys"), pybind11::arg("iMem"));
		cl.def("sizeAll", (int (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::sizeAll, "C++: Pythia8::PartonSystems::sizeAll(int) const --> int", pybind11::arg("iSys"));
		cl.def("getAll", (int (Pythia8::PartonSystems::*)(int, int) const) &Pythia8::PartonSystems::getAll, "C++: Pythia8::PartonSystems::getAll(int, int) const --> int", pybind11::arg("iSys"), pybind11::arg("iMem"));
		cl.def("getSHat", (double (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::getSHat, "C++: Pythia8::PartonSystems::getSHat(int) const --> double", pybind11::arg("iSys"));
		cl.def("getPTHat", (double (Pythia8::PartonSystems::*)(int) const) &Pythia8::PartonSystems::getPTHat, "C++: Pythia8::PartonSystems::getPTHat(int) const --> double", pybind11::arg("iSys"));
		cl.def("getSystemOf", [](Pythia8::PartonSystems const &o, int const & a0) -> int { return o.getSystemOf(a0); }, "", pybind11::arg("iPos"));
		cl.def("getSystemOf", (int (Pythia8::PartonSystems::*)(int, bool) const) &Pythia8::PartonSystems::getSystemOf, "C++: Pythia8::PartonSystems::getSystemOf(int, bool) const --> int", pybind11::arg("iPos"), pybind11::arg("alsoIn"));
		cl.def("getIndexOfOut", (int (Pythia8::PartonSystems::*)(int, int) const) &Pythia8::PartonSystems::getIndexOfOut, "C++: Pythia8::PartonSystems::getIndexOfOut(int, int) const --> int", pybind11::arg("iSys"), pybind11::arg("iPos"));
		cl.def("list", (void (Pythia8::PartonSystems::*)() const) &Pythia8::PartonSystems::list, "C++: Pythia8::PartonSystems::list() const --> void");
		cl.def("popBack", (void (Pythia8::PartonSystems::*)()) &Pythia8::PartonSystems::popBack, "C++: Pythia8::PartonSystems::popBack() --> void");
	}
	{ // Pythia8::NucleonExcitations file:Pythia8/NucleonExcitations.h line:23
		pybind11::class_<Pythia8::NucleonExcitations, std::shared_ptr<Pythia8::NucleonExcitations>, PyCallBack_Pythia8_NucleonExcitations, Pythia8::PhysicsBase> cl(M("Pythia8"), "NucleonExcitations", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::NucleonExcitations(); }, [](){ return new PyCallBack_Pythia8_NucleonExcitations(); } ) );
		cl.def("init", (bool (Pythia8::NucleonExcitations::*)(std::string)) &Pythia8::NucleonExcitations::init, "C++: Pythia8::NucleonExcitations::init(std::string) --> bool", pybind11::arg("path"));
		cl.def("init", (bool (Pythia8::NucleonExcitations::*)(class std::basic_istream<char> &)) &Pythia8::NucleonExcitations::init, "C++: Pythia8::NucleonExcitations::init(class std::basic_istream<char> &) --> bool", pybind11::arg("stream"));
		cl.def("check", (bool (Pythia8::NucleonExcitations::*)()) &Pythia8::NucleonExcitations::check, "C++: Pythia8::NucleonExcitations::check() --> bool");
		cl.def("getExcitationMasks", (class std::vector<int, class std::allocator<int> > (Pythia8::NucleonExcitations::*)() const) &Pythia8::NucleonExcitations::getExcitationMasks, "C++: Pythia8::NucleonExcitations::getExcitationMasks() const --> class std::vector<int, class std::allocator<int> >");
		cl.def("getChannels", (class std::vector<struct std::pair<int, int>, class std::allocator<struct std::pair<int, int> > > (Pythia8::NucleonExcitations::*)() const) &Pythia8::NucleonExcitations::getChannels, "C++: Pythia8::NucleonExcitations::getChannels() const --> class std::vector<struct std::pair<int, int>, class std::allocator<struct std::pair<int, int> > >");
		cl.def("sigmaExTotal", (double (Pythia8::NucleonExcitations::*)(double) const) &Pythia8::NucleonExcitations::sigmaExTotal, "C++: Pythia8::NucleonExcitations::sigmaExTotal(double) const --> double", pybind11::arg("eCM"));
		cl.def("sigmaExPartial", (double (Pythia8::NucleonExcitations::*)(double, int, int) const) &Pythia8::NucleonExcitations::sigmaExPartial, "C++: Pythia8::NucleonExcitations::sigmaExPartial(double, int, int) const --> double", pybind11::arg("eCM"), pybind11::arg("maskC"), pybind11::arg("maskD"));
		cl.def("pickExcitation", (bool (Pythia8::NucleonExcitations::*)(int, int, double, int &, double &, int &, double &)) &Pythia8::NucleonExcitations::pickExcitation, "C++: Pythia8::NucleonExcitations::pickExcitation(int, int, double, int &, double &, int &, double &) --> bool", pybind11::arg("idA"), pybind11::arg("idB"), pybind11::arg("eCM"), pybind11::arg("idCOut"), pybind11::arg("mCOut"), pybind11::arg("idDOut"), pybind11::arg("mDOut"));
		cl.def("sigmaCalc", (double (Pythia8::NucleonExcitations::*)(double) const) &Pythia8::NucleonExcitations::sigmaCalc, "C++: Pythia8::NucleonExcitations::sigmaCalc(double) const --> double", pybind11::arg("eCM"));
		cl.def("sigmaCalc", (double (Pythia8::NucleonExcitations::*)(double, int, int) const) &Pythia8::NucleonExcitations::sigmaCalc, "C++: Pythia8::NucleonExcitations::sigmaCalc(double, int, int) const --> double", pybind11::arg("eCM"), pybind11::arg("maskC"), pybind11::arg("maskD"));
		cl.def("parameterizeAll", [](Pythia8::NucleonExcitations &o, int const & a0) -> bool { return o.parameterizeAll(a0); }, "", pybind11::arg("precision"));
		cl.def("parameterizeAll", (bool (Pythia8::NucleonExcitations::*)(int, double)) &Pythia8::NucleonExcitations::parameterizeAll, "C++: Pythia8::NucleonExcitations::parameterizeAll(int, double) --> bool", pybind11::arg("precision"), pybind11::arg("threshold"));
		cl.def("save", (bool (Pythia8::NucleonExcitations::*)(std::ostream &) const) &Pythia8::NucleonExcitations::save, "C++: Pythia8::NucleonExcitations::save(std::ostream &) const --> bool", pybind11::arg("stream"));
		cl.def("save", [](Pythia8::NucleonExcitations const &o) -> bool { return o.save(); }, "");
		cl.def("save", (bool (Pythia8::NucleonExcitations::*)(std::string) const) &Pythia8::NucleonExcitations::save, "C++: Pythia8::NucleonExcitations::save(std::string) const --> bool", pybind11::arg("file"));
	}
}
