#include <Pythia8/Basics.h>
#include <Pythia8/ColourReconnection.h>
#include <Pythia8/Event.h>
#include <Pythia8/FragmentationFlavZpT.h>
#include <Pythia8/FragmentationSystems.h>
#include <Pythia8/HadronLevel.h>
#include <Pythia8/Info.h>
#include <Pythia8/NucleonExcitations.h>
#include <Pythia8/ParticleData.h>
#include <Pythia8/ParticleDecays.h>
#include <Pythia8/PartonVertex.h>
#include <Pythia8/PhysicsBase.h>
#include <Pythia8/RHadrons.h>
#include <Pythia8/SigmaLowEnergy.h>
#include <Pythia8/StringInteractions.h>
#include <Pythia8/TimeShower.h>
#include <istream>
#include <iterator>
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

// Pythia8::RHadrons file:Pythia8/RHadrons.h line:29
struct PyCallBack_Pythia8_RHadrons : public Pythia8::RHadrons {
	using Pythia8::RHadrons::RHadrons;

	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RHadrons *>(this), "onInitInfoPtr");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RHadrons *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RHadrons *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::RHadrons *>(this), "onStat");
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

// Pythia8::HadronLevel file:Pythia8/HadronLevel.h line:45
struct PyCallBack_Pythia8_HadronLevel : public Pythia8::HadronLevel {
	using Pythia8::HadronLevel::HadronLevel;

	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::HadronLevel *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return HadronLevel::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::HadronLevel *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::HadronLevel *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::HadronLevel *>(this), "onStat");
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

// Pythia8::ColourParticle file:Pythia8/ColourReconnection.h line:142
struct PyCallBack_Pythia8_ColourParticle : public Pythia8::ColourParticle {
	using Pythia8::ColourParticle::ColourParticle;

	int index() const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourParticle *>(this), "index");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::override_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return Particle::index();
	}
};

void bind_Pythia8_RHadrons(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // Pythia8::RHadrons file:Pythia8/RHadrons.h line:29
		pybind11::class_<Pythia8::RHadrons, std::shared_ptr<Pythia8::RHadrons>, PyCallBack_Pythia8_RHadrons, Pythia8::PhysicsBase> cl(M("Pythia8"), "RHadrons", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::RHadrons(); }, [](){ return new PyCallBack_Pythia8_RHadrons(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_RHadrons const &o){ return new PyCallBack_Pythia8_RHadrons(o); } ) );
		cl.def( pybind11::init( [](Pythia8::RHadrons const &o){ return new Pythia8::RHadrons(o); } ) );
		cl.def("init", (bool (Pythia8::RHadrons::*)()) &Pythia8::RHadrons::init, "C++: Pythia8::RHadrons::init() --> bool");
		cl.def("fragPtrs", (void (Pythia8::RHadrons::*)(class Pythia8::StringFlav *, class Pythia8::StringZ *)) &Pythia8::RHadrons::fragPtrs, "C++: Pythia8::RHadrons::fragPtrs(class Pythia8::StringFlav *, class Pythia8::StringZ *) --> void", pybind11::arg("flavSelPtrIn"), pybind11::arg("zSelPtrIn"));
		cl.def("produce", (bool (Pythia8::RHadrons::*)(class Pythia8::ColConfig &, class Pythia8::Event &)) &Pythia8::RHadrons::produce, "C++: Pythia8::RHadrons::produce(class Pythia8::ColConfig &, class Pythia8::Event &) --> bool", pybind11::arg("colConfig"), pybind11::arg("event"));
		cl.def("decay", (bool (Pythia8::RHadrons::*)(class Pythia8::Event &)) &Pythia8::RHadrons::decay, "C++: Pythia8::RHadrons::decay(class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("givesRHadron", (bool (Pythia8::RHadrons::*)(int)) &Pythia8::RHadrons::givesRHadron, "C++: Pythia8::RHadrons::givesRHadron(int) --> bool", pybind11::arg("id"));
		cl.def("exist", (bool (Pythia8::RHadrons::*)()) &Pythia8::RHadrons::exist, "C++: Pythia8::RHadrons::exist() --> bool");
		cl.def("trace", (int (Pythia8::RHadrons::*)(int)) &Pythia8::RHadrons::trace, "C++: Pythia8::RHadrons::trace(int) --> int", pybind11::arg("i"));
		cl.def("assign", (class Pythia8::RHadrons & (Pythia8::RHadrons::*)(const class Pythia8::RHadrons &)) &Pythia8::RHadrons::operator=, "C++: Pythia8::RHadrons::operator=(const class Pythia8::RHadrons &) --> class Pythia8::RHadrons &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::HadronLevel file:Pythia8/HadronLevel.h line:45
		pybind11::class_<Pythia8::HadronLevel, std::shared_ptr<Pythia8::HadronLevel>, PyCallBack_Pythia8_HadronLevel, Pythia8::PhysicsBase> cl(M("Pythia8"), "HadronLevel", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::HadronLevel(); }, [](){ return new PyCallBack_Pythia8_HadronLevel(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_HadronLevel const &o){ return new PyCallBack_Pythia8_HadronLevel(o); } ) );
		cl.def( pybind11::init( [](Pythia8::HadronLevel const &o){ return new Pythia8::HadronLevel(o); } ) );
		cl.def("init", (bool (Pythia8::HadronLevel::*)(class std::shared_ptr<class Pythia8::TimeShower>, class Pythia8::RHadrons *, class std::shared_ptr<class Pythia8::DecayHandler>, class std::vector<int, class std::allocator<int> >, class std::shared_ptr<class Pythia8::StringInteractions>, class std::shared_ptr<class Pythia8::PartonVertex>, class Pythia8::SigmaLowEnergy &, class Pythia8::NucleonExcitations &)) &Pythia8::HadronLevel::init, "C++: Pythia8::HadronLevel::init(class std::shared_ptr<class Pythia8::TimeShower>, class Pythia8::RHadrons *, class std::shared_ptr<class Pythia8::DecayHandler>, class std::vector<int, class std::allocator<int> >, class std::shared_ptr<class Pythia8::StringInteractions>, class std::shared_ptr<class Pythia8::PartonVertex>, class Pythia8::SigmaLowEnergy &, class Pythia8::NucleonExcitations &) --> bool", pybind11::arg("timesDecPtr"), pybind11::arg("rHadronsPtrIn"), pybind11::arg("decayHandlePtr"), pybind11::arg("handledParticles"), pybind11::arg("stringInteractionsPtrIn"), pybind11::arg("partonVertexPtrIn"), pybind11::arg("sigmaLowEnergyIn"), pybind11::arg("nucleonExcitationsIn"));
		cl.def("getStringFlavPtr", (class Pythia8::StringFlav * (Pythia8::HadronLevel::*)()) &Pythia8::HadronLevel::getStringFlavPtr, "C++: Pythia8::HadronLevel::getStringFlavPtr() --> class Pythia8::StringFlav *", pybind11::return_value_policy::automatic);
		cl.def("next", (bool (Pythia8::HadronLevel::*)(class Pythia8::Event &)) &Pythia8::HadronLevel::next, "C++: Pythia8::HadronLevel::next(class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("decay", (bool (Pythia8::HadronLevel::*)(int, class Pythia8::Event &)) &Pythia8::HadronLevel::decay, "C++: Pythia8::HadronLevel::decay(int, class Pythia8::Event &) --> bool", pybind11::arg("iDec"), pybind11::arg("event"));
		cl.def("moreDecays", (bool (Pythia8::HadronLevel::*)(class Pythia8::Event &)) &Pythia8::HadronLevel::moreDecays, "C++: Pythia8::HadronLevel::moreDecays(class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("rescatter", (bool (Pythia8::HadronLevel::*)(class Pythia8::Event &)) &Pythia8::HadronLevel::rescatter, "C++: Pythia8::HadronLevel::rescatter(class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("initLowEnergyProcesses", (bool (Pythia8::HadronLevel::*)()) &Pythia8::HadronLevel::initLowEnergyProcesses, "C++: Pythia8::HadronLevel::initLowEnergyProcesses() --> bool");
		cl.def("pickLowEnergyProcess", (int (Pythia8::HadronLevel::*)(int, int, double, double, double)) &Pythia8::HadronLevel::pickLowEnergyProcess, "C++: Pythia8::HadronLevel::pickLowEnergyProcess(int, int, double, double, double) --> int", pybind11::arg("idA"), pybind11::arg("idB"), pybind11::arg("eCM"), pybind11::arg("mA"), pybind11::arg("mB"));
		cl.def("doLowEnergyProcess", (bool (Pythia8::HadronLevel::*)(int, int, int, class Pythia8::Event &)) &Pythia8::HadronLevel::doLowEnergyProcess, "C++: Pythia8::HadronLevel::doLowEnergyProcess(int, int, int, class Pythia8::Event &) --> bool", pybind11::arg("i1"), pybind11::arg("i2"), pybind11::arg("procTypeIn"), pybind11::arg("event"));
		cl.def("hasVetoedHadronize", (bool (Pythia8::HadronLevel::*)() const) &Pythia8::HadronLevel::hasVetoedHadronize, "C++: Pythia8::HadronLevel::hasVetoedHadronize() const --> bool");
		cl.def("onInitInfoPtr", (void (Pythia8::HadronLevel::*)()) &Pythia8::HadronLevel::onInitInfoPtr, "C++: Pythia8::HadronLevel::onInitInfoPtr() --> void");
		cl.def("assign", (class Pythia8::HadronLevel & (Pythia8::HadronLevel::*)(const class Pythia8::HadronLevel &)) &Pythia8::HadronLevel::operator=, "C++: Pythia8::HadronLevel::operator=(const class Pythia8::HadronLevel &) --> class Pythia8::HadronLevel &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::ColourDipole file:Pythia8/ColourReconnection.h line:36
		pybind11::class_<Pythia8::ColourDipole, std::shared_ptr<Pythia8::ColourDipole>> cl(M("Pythia8"), "ColourDipole", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::ColourDipole(); } ), "doc" );
		cl.def( pybind11::init( [](int const & a0){ return new Pythia8::ColourDipole(a0); } ), "doc" , pybind11::arg("colIn"));
		cl.def( pybind11::init( [](int const & a0, int const & a1){ return new Pythia8::ColourDipole(a0, a1); } ), "doc" , pybind11::arg("colIn"), pybind11::arg("iColIn"));
		cl.def( pybind11::init( [](int const & a0, int const & a1, int const & a2){ return new Pythia8::ColourDipole(a0, a1, a2); } ), "doc" , pybind11::arg("colIn"), pybind11::arg("iColIn"), pybind11::arg("iAcolIn"));
		cl.def( pybind11::init( [](int const & a0, int const & a1, int const & a2, int const & a3){ return new Pythia8::ColourDipole(a0, a1, a2, a3); } ), "doc" , pybind11::arg("colIn"), pybind11::arg("iColIn"), pybind11::arg("iAcolIn"), pybind11::arg("colReconnectionIn"));
		cl.def( pybind11::init( [](int const & a0, int const & a1, int const & a2, int const & a3, bool const & a4){ return new Pythia8::ColourDipole(a0, a1, a2, a3, a4); } ), "doc" , pybind11::arg("colIn"), pybind11::arg("iColIn"), pybind11::arg("iAcolIn"), pybind11::arg("colReconnectionIn"), pybind11::arg("isJunIn"));
		cl.def( pybind11::init( [](int const & a0, int const & a1, int const & a2, int const & a3, bool const & a4, bool const & a5){ return new Pythia8::ColourDipole(a0, a1, a2, a3, a4, a5); } ), "doc" , pybind11::arg("colIn"), pybind11::arg("iColIn"), pybind11::arg("iAcolIn"), pybind11::arg("colReconnectionIn"), pybind11::arg("isJunIn"), pybind11::arg("isAntiJunIn"));
		cl.def( pybind11::init( [](int const & a0, int const & a1, int const & a2, int const & a3, bool const & a4, bool const & a5, bool const & a6){ return new Pythia8::ColourDipole(a0, a1, a2, a3, a4, a5, a6); } ), "doc" , pybind11::arg("colIn"), pybind11::arg("iColIn"), pybind11::arg("iAcolIn"), pybind11::arg("colReconnectionIn"), pybind11::arg("isJunIn"), pybind11::arg("isAntiJunIn"), pybind11::arg("isActiveIn"));
		cl.def( pybind11::init<int, int, int, int, bool, bool, bool, bool>(), pybind11::arg("colIn"), pybind11::arg("iColIn"), pybind11::arg("iAcolIn"), pybind11::arg("colReconnectionIn"), pybind11::arg("isJunIn"), pybind11::arg("isAntiJunIn"), pybind11::arg("isActiveIn"), pybind11::arg("isRealIn") );

		cl.def( pybind11::init( [](Pythia8::ColourDipole const &o){ return new Pythia8::ColourDipole(o); } ) );
		cl.def_readwrite("col", &Pythia8::ColourDipole::col);
		cl.def_readwrite("iCol", &Pythia8::ColourDipole::iCol);
		cl.def_readwrite("iAcol", &Pythia8::ColourDipole::iAcol);
		cl.def_readwrite("iColLeg", &Pythia8::ColourDipole::iColLeg);
		cl.def_readwrite("iAcolLeg", &Pythia8::ColourDipole::iAcolLeg);
		cl.def_readwrite("colReconnection", &Pythia8::ColourDipole::colReconnection);
		cl.def_readwrite("isJun", &Pythia8::ColourDipole::isJun);
		cl.def_readwrite("isAntiJun", &Pythia8::ColourDipole::isAntiJun);
		cl.def_readwrite("isActive", &Pythia8::ColourDipole::isActive);
		cl.def_readwrite("isReal", &Pythia8::ColourDipole::isReal);
		cl.def_readwrite("printed", &Pythia8::ColourDipole::printed);
		cl.def_readwrite("leftDip", &Pythia8::ColourDipole::leftDip);
		cl.def_readwrite("rightDip", &Pythia8::ColourDipole::rightDip);
		cl.def_readwrite("colDips", &Pythia8::ColourDipole::colDips);
		cl.def_readwrite("acolDips", &Pythia8::ColourDipole::acolDips);
		cl.def_readwrite("p1p2", &Pythia8::ColourDipole::p1p2);
		cl.def_readwrite("dipoleMomentum", &Pythia8::ColourDipole::dipoleMomentum);
		cl.def_readwrite("ciCol", &Pythia8::ColourDipole::ciCol);
		cl.def_readwrite("ciAcol", &Pythia8::ColourDipole::ciAcol);
		cl.def_readwrite("pCalculated", &Pythia8::ColourDipole::pCalculated);
		cl.def_readwrite("index", &Pythia8::ColourDipole::index);
		cl.def("mDip", (double (Pythia8::ColourDipole::*)(class Pythia8::Event &)) &Pythia8::ColourDipole::mDip, "C++: Pythia8::ColourDipole::mDip(class Pythia8::Event &) --> double", pybind11::arg("event"));
		cl.def("list", (void (Pythia8::ColourDipole::*)() const) &Pythia8::ColourDipole::list, "C++: Pythia8::ColourDipole::list() const --> void");
	}
	{ // Pythia8::ColourJunction file:Pythia8/ColourReconnection.h line:80
		pybind11::class_<Pythia8::ColourJunction, std::shared_ptr<Pythia8::ColourJunction>, Pythia8::Junction> cl(M("Pythia8"), "ColourJunction", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init<const class Pythia8::Junction &>(), pybind11::arg("ju") );

		cl.def( pybind11::init( [](Pythia8::ColourJunction const &o){ return new Pythia8::ColourJunction(o); } ) );
		cl.def("assign", (class Pythia8::ColourJunction & (Pythia8::ColourJunction::*)(const class Pythia8::ColourJunction &)) &Pythia8::ColourJunction::operator=, "C++: Pythia8::ColourJunction::operator=(const class Pythia8::ColourJunction &) --> class Pythia8::ColourJunction &", pybind11::return_value_policy::reference, pybind11::arg("ju"));
		cl.def("getColDip", (class std::shared_ptr<class Pythia8::ColourDipole> (Pythia8::ColourJunction::*)(int)) &Pythia8::ColourJunction::getColDip, "C++: Pythia8::ColourJunction::getColDip(int) --> class std::shared_ptr<class Pythia8::ColourDipole>", pybind11::arg("i"));
		cl.def("setColDip", (void (Pythia8::ColourJunction::*)(int, class std::shared_ptr<class Pythia8::ColourDipole>)) &Pythia8::ColourJunction::setColDip, "C++: Pythia8::ColourJunction::setColDip(int, class std::shared_ptr<class Pythia8::ColourDipole>) --> void", pybind11::arg("i"), pybind11::arg("dip"));
		cl.def("list", (void (Pythia8::ColourJunction::*)() const) &Pythia8::ColourJunction::list, "C++: Pythia8::ColourJunction::list() const --> void");
	}
	{ // Pythia8::TrialReconnection file:Pythia8/ColourReconnection.h line:112
		pybind11::class_<Pythia8::TrialReconnection, std::shared_ptr<Pythia8::TrialReconnection>> cl(M("Pythia8"), "TrialReconnection", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::TrialReconnection(); } ), "doc" );
		cl.def( pybind11::init( [](class std::shared_ptr<class Pythia8::ColourDipole> const & a0){ return new Pythia8::TrialReconnection(a0); } ), "doc" , pybind11::arg("dip1In"));
		cl.def( pybind11::init( [](class std::shared_ptr<class Pythia8::ColourDipole> const & a0, class std::shared_ptr<class Pythia8::ColourDipole> const & a1){ return new Pythia8::TrialReconnection(a0, a1); } ), "doc" , pybind11::arg("dip1In"), pybind11::arg("dip2In"));
		cl.def( pybind11::init( [](class std::shared_ptr<class Pythia8::ColourDipole> const & a0, class std::shared_ptr<class Pythia8::ColourDipole> const & a1, class std::shared_ptr<class Pythia8::ColourDipole> const & a2){ return new Pythia8::TrialReconnection(a0, a1, a2); } ), "doc" , pybind11::arg("dip1In"), pybind11::arg("dip2In"), pybind11::arg("dip3In"));
		cl.def( pybind11::init( [](class std::shared_ptr<class Pythia8::ColourDipole> const & a0, class std::shared_ptr<class Pythia8::ColourDipole> const & a1, class std::shared_ptr<class Pythia8::ColourDipole> const & a2, class std::shared_ptr<class Pythia8::ColourDipole> const & a3){ return new Pythia8::TrialReconnection(a0, a1, a2, a3); } ), "doc" , pybind11::arg("dip1In"), pybind11::arg("dip2In"), pybind11::arg("dip3In"), pybind11::arg("dip4In"));
		cl.def( pybind11::init( [](class std::shared_ptr<class Pythia8::ColourDipole> const & a0, class std::shared_ptr<class Pythia8::ColourDipole> const & a1, class std::shared_ptr<class Pythia8::ColourDipole> const & a2, class std::shared_ptr<class Pythia8::ColourDipole> const & a3, int const & a4){ return new Pythia8::TrialReconnection(a0, a1, a2, a3, a4); } ), "doc" , pybind11::arg("dip1In"), pybind11::arg("dip2In"), pybind11::arg("dip3In"), pybind11::arg("dip4In"), pybind11::arg("modeIn"));
		cl.def( pybind11::init<class std::shared_ptr<class Pythia8::ColourDipole>, class std::shared_ptr<class Pythia8::ColourDipole>, class std::shared_ptr<class Pythia8::ColourDipole>, class std::shared_ptr<class Pythia8::ColourDipole>, int, double>(), pybind11::arg("dip1In"), pybind11::arg("dip2In"), pybind11::arg("dip3In"), pybind11::arg("dip4In"), pybind11::arg("modeIn"), pybind11::arg("lambdaDiffIn") );

		cl.def_readwrite("dips", &Pythia8::TrialReconnection::dips);
		cl.def_readwrite("mode", &Pythia8::TrialReconnection::mode);
		cl.def_readwrite("lambdaDiff", &Pythia8::TrialReconnection::lambdaDiff);
		cl.def("list", (void (Pythia8::TrialReconnection::*)()) &Pythia8::TrialReconnection::list, "C++: Pythia8::TrialReconnection::list() --> void");
	}
	{ // Pythia8::ColourParticle file:Pythia8/ColourReconnection.h line:142
		pybind11::class_<Pythia8::ColourParticle, std::shared_ptr<Pythia8::ColourParticle>, PyCallBack_Pythia8_ColourParticle, Pythia8::Particle> cl(M("Pythia8"), "ColourParticle", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init<const class Pythia8::Particle &>(), pybind11::arg("ju") );

		cl.def_readwrite("dips", &Pythia8::ColourParticle::dips);
		cl.def_readwrite("colEndIncluded", &Pythia8::ColourParticle::colEndIncluded);
		cl.def_readwrite("acolEndIncluded", &Pythia8::ColourParticle::acolEndIncluded);
		cl.def_readwrite("activeDips", &Pythia8::ColourParticle::activeDips);
		cl.def_readwrite("isJun", &Pythia8::ColourParticle::isJun);
		cl.def_readwrite("junKind", &Pythia8::ColourParticle::junKind);
		cl.def("listParticle", (void (Pythia8::ColourParticle::*)()) &Pythia8::ColourParticle::listParticle, "C++: Pythia8::ColourParticle::listParticle() --> void");
		cl.def("listActiveDips", (void (Pythia8::ColourParticle::*)()) &Pythia8::ColourParticle::listActiveDips, "C++: Pythia8::ColourParticle::listActiveDips() --> void");
		cl.def("listDips", (void (Pythia8::ColourParticle::*)()) &Pythia8::ColourParticle::listDips, "C++: Pythia8::ColourParticle::listDips() --> void");
		cl.def("assign", (class Pythia8::ColourParticle & (Pythia8::ColourParticle::*)(const class Pythia8::ColourParticle &)) &Pythia8::ColourParticle::operator=, "C++: Pythia8::ColourParticle::operator=(const class Pythia8::ColourParticle &) --> class Pythia8::ColourParticle &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
}
