#include <Pythia8/Basics.h>
#include <Pythia8/BeamParticle.h>
#include <Pythia8/BeamRemnants.h>
#include <Pythia8/BeamSetup.h>
#include <Pythia8/ColourReconnection.h>
#include <Pythia8/Event.h>
#include <Pythia8/FragmentationFlavZpT.h>
#include <Pythia8/HadronWidths.h>
#include <Pythia8/Info.h>
#include <Pythia8/LHEF3.h>
#include <Pythia8/Logger.h>
#include <Pythia8/MultipartonInteractions.h>
#include <Pythia8/ParticleData.h>
#include <Pythia8/PartonDistributions.h>
#include <Pythia8/PartonSystems.h>
#include <Pythia8/PartonVertex.h>
#include <Pythia8/PhysicsBase.h>
#include <Pythia8/ResonanceWidths.h>
#include <Pythia8/Settings.h>
#include <Pythia8/SigmaLowEnergy.h>
#include <Pythia8/SigmaProcess.h>
#include <Pythia8/SigmaTotal.h>
#include <Pythia8/StandardModel.h>
#include <Pythia8/StringInteractions.h>
#include <Pythia8/SusyCouplings.h>
#include <Pythia8/Weights.h>
#include <functional>
#include <istream>
#include <iterator>
#include <map>
#include <memory>
#include <ostream>
#include <sstream> // __str__
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

// Pythia8::ColourReconnection file:Pythia8/ColourReconnection.h line:167
struct PyCallBack_Pythia8_ColourReconnection : public Pythia8::ColourReconnection {
	using Pythia8::ColourReconnection::ColourReconnection;

	bool init() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnection *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return ColourReconnection::init();
	}
	void reassignBeamPtrs(class Pythia8::BeamParticle * a0, class Pythia8::BeamParticle * a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnection *>(this), "reassignBeamPtrs");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return ColourReconnection::reassignBeamPtrs(a0, a1);
	}
	bool next(class Pythia8::Event & a0, int a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnection *>(this), "next");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return ColourReconnection::next(a0, a1);
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnection *>(this), "onInitInfoPtr");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnection *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnection *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnection *>(this), "onStat");
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

// Pythia8::BeamRemnants file:Pythia8/BeamRemnants.h line:35
struct PyCallBack_Pythia8_BeamRemnants : public Pythia8::BeamRemnants {
	using Pythia8::BeamRemnants::BeamRemnants;

	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::BeamRemnants *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return BeamRemnants::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::BeamRemnants *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::BeamRemnants *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::BeamRemnants *>(this), "onStat");
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

// Pythia8::MultipartonInteractions file:Pythia8/MultipartonInteractions.h line:100
struct PyCallBack_Pythia8_MultipartonInteractions : public Pythia8::MultipartonInteractions {
	using Pythia8::MultipartonInteractions::MultipartonInteractions;

	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::MultipartonInteractions *>(this), "onInitInfoPtr");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::MultipartonInteractions *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::MultipartonInteractions *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::MultipartonInteractions *>(this), "onStat");
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

void bind_Pythia8_ColourReconnection(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // Pythia8::ColourReconnection file:Pythia8/ColourReconnection.h line:167
		pybind11::class_<Pythia8::ColourReconnection, std::shared_ptr<Pythia8::ColourReconnection>, PyCallBack_Pythia8_ColourReconnection, Pythia8::ColourReconnectionBase> cl(M("Pythia8"), "ColourReconnection", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::ColourReconnection(); }, [](){ return new PyCallBack_Pythia8_ColourReconnection(); } ) );
		cl.def("init", (bool (Pythia8::ColourReconnection::*)()) &Pythia8::ColourReconnection::init, "C++: Pythia8::ColourReconnection::init() --> bool");
		cl.def("reassignBeamPtrs", (void (Pythia8::ColourReconnection::*)(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *)) &Pythia8::ColourReconnection::reassignBeamPtrs, "C++: Pythia8::ColourReconnection::reassignBeamPtrs(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *) --> void", pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"));
		cl.def("next", (bool (Pythia8::ColourReconnection::*)(class Pythia8::Event &, int)) &Pythia8::ColourReconnection::next, "C++: Pythia8::ColourReconnection::next(class Pythia8::Event &, int) --> bool", pybind11::arg("event"), pybind11::arg("oldSize"));
		cl.def("assign", (class Pythia8::ColourReconnection & (Pythia8::ColourReconnection::*)(const class Pythia8::ColourReconnection &)) &Pythia8::ColourReconnection::operator=, "C++: Pythia8::ColourReconnection::operator=(const class Pythia8::ColourReconnection &) --> class Pythia8::ColourReconnection &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::BeamRemnants file:Pythia8/BeamRemnants.h line:35
		pybind11::class_<Pythia8::BeamRemnants, std::shared_ptr<Pythia8::BeamRemnants>, PyCallBack_Pythia8_BeamRemnants, Pythia8::PhysicsBase> cl(M("Pythia8"), "BeamRemnants", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::BeamRemnants(); }, [](){ return new PyCallBack_Pythia8_BeamRemnants(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_BeamRemnants const &o){ return new PyCallBack_Pythia8_BeamRemnants(o); } ) );
		cl.def( pybind11::init( [](Pythia8::BeamRemnants const &o){ return new Pythia8::BeamRemnants(o); } ) );
		cl.def("init", (bool (Pythia8::BeamRemnants::*)(class std::shared_ptr<class Pythia8::PartonVertex>, class std::shared_ptr<class Pythia8::ColourReconnectionBase>)) &Pythia8::BeamRemnants::init, "C++: Pythia8::BeamRemnants::init(class std::shared_ptr<class Pythia8::PartonVertex>, class std::shared_ptr<class Pythia8::ColourReconnectionBase>) --> bool", pybind11::arg("partonVertexPtrIn"), pybind11::arg("colourReconnectionPtrIn"));
		cl.def("reassignBeamPtrs", (void (Pythia8::BeamRemnants::*)(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *, int)) &Pythia8::BeamRemnants::reassignBeamPtrs, "C++: Pythia8::BeamRemnants::reassignBeamPtrs(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *, int) --> void", pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"), pybind11::arg("iDSin"));
		cl.def("add", [](Pythia8::BeamRemnants &o, class Pythia8::Event & a0) -> bool { return o.add(a0); }, "", pybind11::arg("event"));
		cl.def("add", [](Pythia8::BeamRemnants &o, class Pythia8::Event & a0, int const & a1) -> bool { return o.add(a0, a1); }, "", pybind11::arg("event"), pybind11::arg("iFirst"));
		cl.def("add", (bool (Pythia8::BeamRemnants::*)(class Pythia8::Event &, int, bool)) &Pythia8::BeamRemnants::add, "C++: Pythia8::BeamRemnants::add(class Pythia8::Event &, int, bool) --> bool", pybind11::arg("event"), pybind11::arg("iFirst"), pybind11::arg("doDiffCR"));
		cl.def("onInitInfoPtr", (void (Pythia8::BeamRemnants::*)()) &Pythia8::BeamRemnants::onInitInfoPtr, "C++: Pythia8::BeamRemnants::onInitInfoPtr() --> void");
		cl.def("assign", (class Pythia8::BeamRemnants & (Pythia8::BeamRemnants::*)(const class Pythia8::BeamRemnants &)) &Pythia8::BeamRemnants::operator=, "C++: Pythia8::BeamRemnants::operator=(const class Pythia8::BeamRemnants &) --> class Pythia8::BeamRemnants &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::SigmaMultiparton file:Pythia8/MultipartonInteractions.h line:35
		pybind11::class_<Pythia8::SigmaMultiparton, std::shared_ptr<Pythia8::SigmaMultiparton>> cl(M("Pythia8"), "SigmaMultiparton", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::SigmaMultiparton(); } ) );
		cl.def( pybind11::init( [](Pythia8::SigmaMultiparton const &o){ return new Pythia8::SigmaMultiparton(o); } ) );
		cl.def("init", (bool (Pythia8::SigmaMultiparton::*)(int, int, class Pythia8::Info *, class Pythia8::BeamParticle *, class Pythia8::BeamParticle *)) &Pythia8::SigmaMultiparton::init, "C++: Pythia8::SigmaMultiparton::init(int, int, class Pythia8::Info *, class Pythia8::BeamParticle *, class Pythia8::BeamParticle *) --> bool", pybind11::arg("inState"), pybind11::arg("processLevel"), pybind11::arg("infoPtr"), pybind11::arg("beamAPtr"), pybind11::arg("beamBPtr"));
		cl.def("updateBeamIDs", (void (Pythia8::SigmaMultiparton::*)()) &Pythia8::SigmaMultiparton::updateBeamIDs, "C++: Pythia8::SigmaMultiparton::updateBeamIDs() --> void");
		cl.def("sigma", [](Pythia8::SigmaMultiparton &o, int const & a0, int const & a1, double const & a2, double const & a3, double const & a4, double const & a5, double const & a6, double const & a7, double const & a8) -> double { return o.sigma(a0, a1, a2, a3, a4, a5, a6, a7, a8); }, "", pybind11::arg("id1"), pybind11::arg("id2"), pybind11::arg("x1"), pybind11::arg("x2"), pybind11::arg("sHat"), pybind11::arg("tHat"), pybind11::arg("uHat"), pybind11::arg("alpS"), pybind11::arg("alpEM"));
		cl.def("sigma", [](Pythia8::SigmaMultiparton &o, int const & a0, int const & a1, double const & a2, double const & a3, double const & a4, double const & a5, double const & a6, double const & a7, double const & a8, bool const & a9) -> double { return o.sigma(a0, a1, a2, a3, a4, a5, a6, a7, a8, a9); }, "", pybind11::arg("id1"), pybind11::arg("id2"), pybind11::arg("x1"), pybind11::arg("x2"), pybind11::arg("sHat"), pybind11::arg("tHat"), pybind11::arg("uHat"), pybind11::arg("alpS"), pybind11::arg("alpEM"), pybind11::arg("restore"));
		cl.def("sigma", (double (Pythia8::SigmaMultiparton::*)(int, int, double, double, double, double, double, double, double, bool, bool)) &Pythia8::SigmaMultiparton::sigma, "C++: Pythia8::SigmaMultiparton::sigma(int, int, double, double, double, double, double, double, double, bool, bool) --> double", pybind11::arg("id1"), pybind11::arg("id2"), pybind11::arg("x1"), pybind11::arg("x2"), pybind11::arg("sHat"), pybind11::arg("tHat"), pybind11::arg("uHat"), pybind11::arg("alpS"), pybind11::arg("alpEM"), pybind11::arg("restore"), pybind11::arg("pickOtherIn"));
		cl.def("pickedOther", (bool (Pythia8::SigmaMultiparton::*)()) &Pythia8::SigmaMultiparton::pickedOther, "C++: Pythia8::SigmaMultiparton::pickedOther() --> bool");
		cl.def("sigmaSel", (class std::shared_ptr<class Pythia8::SigmaProcess> (Pythia8::SigmaMultiparton::*)()) &Pythia8::SigmaMultiparton::sigmaSel, "C++: Pythia8::SigmaMultiparton::sigmaSel() --> class std::shared_ptr<class Pythia8::SigmaProcess>");
		cl.def("swapTU", (bool (Pythia8::SigmaMultiparton::*)()) &Pythia8::SigmaMultiparton::swapTU, "C++: Pythia8::SigmaMultiparton::swapTU() --> bool");
		cl.def("nProc", (int (Pythia8::SigmaMultiparton::*)() const) &Pythia8::SigmaMultiparton::nProc, "C++: Pythia8::SigmaMultiparton::nProc() const --> int");
		cl.def("codeProc", (int (Pythia8::SigmaMultiparton::*)(int) const) &Pythia8::SigmaMultiparton::codeProc, "C++: Pythia8::SigmaMultiparton::codeProc(int) const --> int", pybind11::arg("iProc"));
		cl.def("nameProc", (std::string (Pythia8::SigmaMultiparton::*)(int) const) &Pythia8::SigmaMultiparton::nameProc, "C++: Pythia8::SigmaMultiparton::nameProc(int) const --> std::string", pybind11::arg("iProc"));
		cl.def("assign", (class Pythia8::SigmaMultiparton & (Pythia8::SigmaMultiparton::*)(const class Pythia8::SigmaMultiparton &)) &Pythia8::SigmaMultiparton::operator=, "C++: Pythia8::SigmaMultiparton::operator=(const class Pythia8::SigmaMultiparton &) --> class Pythia8::SigmaMultiparton &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::MultipartonInteractions file:Pythia8/MultipartonInteractions.h line:100
		pybind11::class_<Pythia8::MultipartonInteractions, std::shared_ptr<Pythia8::MultipartonInteractions>, PyCallBack_Pythia8_MultipartonInteractions, Pythia8::PhysicsBase> cl(M("Pythia8"), "MultipartonInteractions", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::MultipartonInteractions(); }, [](){ return new PyCallBack_Pythia8_MultipartonInteractions(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_MultipartonInteractions const &o){ return new PyCallBack_Pythia8_MultipartonInteractions(o); } ) );
		cl.def( pybind11::init( [](Pythia8::MultipartonInteractions const &o){ return new Pythia8::MultipartonInteractions(o); } ) );
		cl.def("init", [](Pythia8::MultipartonInteractions &o, bool const & a0, int const & a1, class Pythia8::BeamParticle * a2, class Pythia8::BeamParticle * a3, class std::shared_ptr<class Pythia8::PartonVertex> const & a4) -> bool { return o.init(a0, a1, a2, a3, a4); }, "", pybind11::arg("doMPIinit"), pybind11::arg("iDiffSysIn"), pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"), pybind11::arg("partonVertexPtrIn"));
		cl.def("init", (bool (Pythia8::MultipartonInteractions::*)(bool, int, class Pythia8::BeamParticle *, class Pythia8::BeamParticle *, class std::shared_ptr<class Pythia8::PartonVertex>, bool)) &Pythia8::MultipartonInteractions::init, "C++: Pythia8::MultipartonInteractions::init(bool, int, class Pythia8::BeamParticle *, class Pythia8::BeamParticle *, class std::shared_ptr<class Pythia8::PartonVertex>, bool) --> bool", pybind11::arg("doMPIinit"), pybind11::arg("iDiffSysIn"), pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"), pybind11::arg("partonVertexPtrIn"), pybind11::arg("hasGammaIn"));
		cl.def("initSwitchID", (void (Pythia8::MultipartonInteractions::*)(const class std::vector<int, class std::allocator<int> > &)) &Pythia8::MultipartonInteractions::initSwitchID, "C++: Pythia8::MultipartonInteractions::initSwitchID(const class std::vector<int, class std::allocator<int> > &) --> void", pybind11::arg("idAListIn"));
		cl.def("setBeamID", (void (Pythia8::MultipartonInteractions::*)(int)) &Pythia8::MultipartonInteractions::setBeamID, "C++: Pythia8::MultipartonInteractions::setBeamID(int) --> void", pybind11::arg("iPDFAin"));
		cl.def("reset", (void (Pythia8::MultipartonInteractions::*)()) &Pythia8::MultipartonInteractions::reset, "C++: Pythia8::MultipartonInteractions::reset() --> void");
		cl.def("pTfirst", (void (Pythia8::MultipartonInteractions::*)()) &Pythia8::MultipartonInteractions::pTfirst, "C++: Pythia8::MultipartonInteractions::pTfirst() --> void");
		cl.def("setupFirstSys", (void (Pythia8::MultipartonInteractions::*)(class Pythia8::Event &)) &Pythia8::MultipartonInteractions::setupFirstSys, "C++: Pythia8::MultipartonInteractions::setupFirstSys(class Pythia8::Event &) --> void", pybind11::arg("process"));
		cl.def("limitPTmax", (bool (Pythia8::MultipartonInteractions::*)(class Pythia8::Event &)) &Pythia8::MultipartonInteractions::limitPTmax, "C++: Pythia8::MultipartonInteractions::limitPTmax(class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("scaleLimitPT", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::scaleLimitPT, "C++: Pythia8::MultipartonInteractions::scaleLimitPT() const --> double");
		cl.def("prepare", [](Pythia8::MultipartonInteractions &o, class Pythia8::Event & a0) -> void { return o.prepare(a0); }, "", pybind11::arg("event"));
		cl.def("prepare", [](Pythia8::MultipartonInteractions &o, class Pythia8::Event & a0, double const & a1) -> void { return o.prepare(a0, a1); }, "", pybind11::arg("event"), pybind11::arg("pTscale"));
		cl.def("prepare", (void (Pythia8::MultipartonInteractions::*)(class Pythia8::Event &, double, bool)) &Pythia8::MultipartonInteractions::prepare, "C++: Pythia8::MultipartonInteractions::prepare(class Pythia8::Event &, double, bool) --> void", pybind11::arg("event"), pybind11::arg("pTscale"), pybind11::arg("rehashB"));
		cl.def("pTnext", (double (Pythia8::MultipartonInteractions::*)(double, double, class Pythia8::Event &)) &Pythia8::MultipartonInteractions::pTnext, "C++: Pythia8::MultipartonInteractions::pTnext(double, double, class Pythia8::Event &) --> double", pybind11::arg("pTbegAll"), pybind11::arg("pTendAll"), pybind11::arg("event"));
		cl.def("scatter", (bool (Pythia8::MultipartonInteractions::*)(class Pythia8::Event &)) &Pythia8::MultipartonInteractions::scatter, "C++: Pythia8::MultipartonInteractions::scatter(class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("setEmpty", (void (Pythia8::MultipartonInteractions::*)()) &Pythia8::MultipartonInteractions::setEmpty, "C++: Pythia8::MultipartonInteractions::setEmpty() --> void");
		cl.def("Q2Ren", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::Q2Ren, "C++: Pythia8::MultipartonInteractions::Q2Ren() const --> double");
		cl.def("alphaSH", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::alphaSH, "C++: Pythia8::MultipartonInteractions::alphaSH() const --> double");
		cl.def("alphaEMH", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::alphaEMH, "C++: Pythia8::MultipartonInteractions::alphaEMH() const --> double");
		cl.def("x1H", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::x1H, "C++: Pythia8::MultipartonInteractions::x1H() const --> double");
		cl.def("x2H", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::x2H, "C++: Pythia8::MultipartonInteractions::x2H() const --> double");
		cl.def("Q2Fac", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::Q2Fac, "C++: Pythia8::MultipartonInteractions::Q2Fac() const --> double");
		cl.def("pdf1", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::pdf1, "C++: Pythia8::MultipartonInteractions::pdf1() const --> double");
		cl.def("pdf2", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::pdf2, "C++: Pythia8::MultipartonInteractions::pdf2() const --> double");
		cl.def("bMPI", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::bMPI, "C++: Pythia8::MultipartonInteractions::bMPI() const --> double");
		cl.def("enhanceMPI", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::enhanceMPI, "C++: Pythia8::MultipartonInteractions::enhanceMPI() const --> double");
		cl.def("enhanceMPIavg", (double (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::enhanceMPIavg, "C++: Pythia8::MultipartonInteractions::enhanceMPIavg() const --> double");
		cl.def("getVSC1", (int (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::getVSC1, "C++: Pythia8::MultipartonInteractions::getVSC1() const --> int");
		cl.def("getVSC2", (int (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::getVSC2, "C++: Pythia8::MultipartonInteractions::getVSC2() const --> int");
		cl.def("getBeamOffset", (int (Pythia8::MultipartonInteractions::*)() const) &Pythia8::MultipartonInteractions::getBeamOffset, "C++: Pythia8::MultipartonInteractions::getBeamOffset() const --> int");
		cl.def("setBeamOffset", (void (Pythia8::MultipartonInteractions::*)(int)) &Pythia8::MultipartonInteractions::setBeamOffset, "C++: Pythia8::MultipartonInteractions::setBeamOffset(int) --> void", pybind11::arg("offsetIn"));
		cl.def("accumulate", (void (Pythia8::MultipartonInteractions::*)()) &Pythia8::MultipartonInteractions::accumulate, "C++: Pythia8::MultipartonInteractions::accumulate() --> void");
		cl.def("statistics", [](Pythia8::MultipartonInteractions &o) -> void { return o.statistics(); }, "");
		cl.def("statistics", (void (Pythia8::MultipartonInteractions::*)(bool)) &Pythia8::MultipartonInteractions::statistics, "C++: Pythia8::MultipartonInteractions::statistics(bool) --> void", pybind11::arg("resetStat"));
		cl.def("resetStatistics", (void (Pythia8::MultipartonInteractions::*)()) &Pythia8::MultipartonInteractions::resetStatistics, "C++: Pythia8::MultipartonInteractions::resetStatistics() --> void");
		cl.def("assign", (class Pythia8::MultipartonInteractions & (Pythia8::MultipartonInteractions::*)(const class Pythia8::MultipartonInteractions &)) &Pythia8::MultipartonInteractions::operator=, "C++: Pythia8::MultipartonInteractions::operator=(const class Pythia8::MultipartonInteractions &) --> class Pythia8::MultipartonInteractions &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
}
